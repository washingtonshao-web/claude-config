export const meta = {
  name: 'deep-research',
  description: 'Deep research: plan, parallel researchers, gap check, report, independent Opus review and fix',
  whenToUse: 'The user says "deep research" / 深度研究 / /deep-research about a topic or question',
  phases: [
    { title: 'Plan', detail: 'split the question into sub-questions' },
    { title: 'Research', detail: 'one agent per sub-question' },
    { title: 'Gaps', detail: 'completeness critic + gap-fill researchers' },
    { title: 'Write', detail: 'synthesize report.md' },
    { title: 'Review', detail: 'independent Opus high-effort review', model: 'opus' },
    { title: 'Fix', detail: 'apply review findings' },
  ],
}

// args: plain question text, or { question, out_dir, date, language, max_researchers }
const A = typeof args === 'string' ? { question: args } : (args || {})
if (!A.question) throw new Error('A research question is required')
const Q = A.question
let DATE = A.date || ''
const LANG = A.language || 'the language the question is written in'

const PLAN = {
  type: 'object',
  properties: {
    framing: { type: 'string', description: 'What the user most likely needs answered, scope, key assumptions' },
    sub_questions: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'short kebab-case id' },
          question: { type: 'string' },
          angle: { type: 'string', description: 'search angle and the numbers to look for' },
          sources_hint: { type: 'string' },
        },
        required: ['id', 'question', 'angle'],
      },
    },
    outline: { type: 'array', items: { type: 'string' }, description: 'report section headings' },
    today: { type: 'string', description: 'today, YYYY-MM-DD' },
    slug: { type: 'string', description: '2-4 English words, kebab-case, naming the topic' },
  },
  required: ['framing', 'sub_questions', 'outline', 'today', 'slug'],
}

const FINDINGS = {
  type: 'object',
  properties: {
    summary: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          claim: { type: 'string' },
          kind: { type: 'string', enum: ['fact', 'estimate', 'inference'] },
          numbers: { type: 'string' },
          sources: { type: 'array', items: { type: 'string' }, description: 'URL, PMID, DOI or NCT id, with date' },
          confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
        },
        required: ['claim', 'kind', 'sources', 'confidence'],
      },
    },
    open_questions: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['summary', 'findings'],
}

const GAPS = {
  type: 'object',
  properties: {
    gaps: {
      type: 'array',
      items: {
        type: 'object',
        properties: { id: { type: 'string' }, question: { type: 'string' }, angle: { type: 'string' } },
        required: ['id', 'question', 'angle'],
      },
    },
  },
  required: ['gaps'],
}

const REVIEW = {
  type: 'object',
  properties: {
    verdict: { type: 'string' },
    issues: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
          location: { type: 'string' },
          problem: { type: 'string' },
          fix: { type: 'string' },
        },
        required: ['severity', 'problem', 'fix'],
      },
    },
  },
  required: ['verdict', 'issues'],
}

const researchPrompt = (s) => `You are one researcher in a deep-research team. Today: ${DATE}.
Overall question: ${Q}
Your sub-question (${s.id}): ${s.question}
Angle: ${s.angle}${s.sources_hint ? `\nSource hints: ${s.sources_hint}` : ''}

Research thoroughly, preferring WebSearch / WebFetch / PubMed tools over browsers: WebSearch (use mode "extended" for niche, recent or numeric facts), read primary sources with WebFetch, use PubMed / Europe PMC / ClinicalTrials tools for biomedical topics. Prefer primary and recent sources; note the date of every number. Get concrete numbers wherever they exist. Label each finding fact / estimate / inference. Do not write files. Return only the structured result.`

const runResearch = (items, phaseName) => pipeline(items, (s) =>
  agent(researchPrompt(s), { label: `research:${s.id}`, phase: phaseName, schema: FINDINGS }))

// ---------- Plan ----------
phase('Plan')
const plan = await agent(`Plan a deep-research effort. Today: ${DATE || 'unknown - run Get-Date to find it'}.
Question: ${Q}

Decide what the user most likely needs (infer scope; do not ask). Split it into independent sub-questions that together answer it fully: usually 6-15, fewer for narrow questions. Each must be researchable on its own, with a specific angle and the numbers to find. Also give a report outline.${A.max_researchers ? `\nUse at most ${A.max_researchers} sub-questions.` : ''}`, { label: 'planner', schema: PLAN })

DATE = DATE || plan.today
// Relative paths resolve against the session's project folder.
const OUT = (A.out_dir || `research/${DATE.replace(/-/g, '').slice(2)}-${plan.slug}`).replace(/\\/g, '/').replace(/\/$/, '')
log(`Report folder: ${OUT}`)

let subs = plan.sub_questions
if (A.max_researchers && subs.length > A.max_researchers) {
  log(`Planner returned ${subs.length} sub-questions; keeping ${A.max_researchers} (user cap). Dropped: ${subs.slice(A.max_researchers).map(s => s.id).join(', ')}`)
  subs = subs.slice(0, A.max_researchers)
}
log(`${subs.length} sub-questions: ${subs.map(s => s.id).join(', ')}`)

// ---------- Research ----------
phase('Research')
const r1 = await runResearch(subs, 'Research')
const results = subs.map((s, i) => ({ sub: s, res: r1[i] }))
const failed = results.filter(x => !x.res).map(x => x.sub.id)
if (failed.length) log(`Researchers that returned nothing: ${failed.join(', ')}`)

// ---------- Gaps ----------
phase('Gaps')
let gapResults = []
{
  const digest = results.filter(x => x.res).map(x => ({ id: x.sub.id, question: x.sub.question, summary: x.res.summary, open_questions: x.res.open_questions || [] }))
  const gaps = await agent(`You are the completeness critic for a deep-research effort.
Question: ${Q}
Framing: ${plan.framing}
What the researchers found (summaries): ${JSON.stringify(digest)}

List only material gaps: an important part of the question not covered, a key number missing, a claim resting on one weak source, or an obvious counter-view not examined. At most 5; return an empty list if coverage is good.`, { label: 'gap-critic', schema: GAPS })
  if (gaps.gaps.length) {
    log(`Gap-fill: ${gaps.gaps.map(g => g.id).join(', ')}`)
    const r2 = await runResearch(gaps.gaps, 'Gaps')
    gapResults = gaps.gaps.map((g, i) => ({ sub: g, res: r2[i] })).filter(x => x.res)
  }
}

const allFindings = results.concat(gapResults)
  .filter(x => x.res)
  .map(x => ({ id: x.sub.id, question: x.sub.question, summary: x.res.summary, findings: x.res.findings, open_questions: x.res.open_questions || [] }))

// ---------- Write ----------
phase('Write')
await agent(`Write the final deep-research report. Today: ${DATE}.
Question: ${Q}
Framing: ${plan.framing}
Suggested outline: ${JSON.stringify(plan.outline)}
Research findings (JSON): ${JSON.stringify(allFindings)}
${failed.length ? `Not researched (researcher returned nothing): ${failed.join(', ')}. State this gap in the report.` : ''}

Write it in ${LANG} to ${OUT}/report.md (create the folder if needed). Structure: the answer and recommendation first; then a key-numbers table; then sections; mark each claim as fact, estimate or inference where it matters; resolve conflicting numbers explicitly; end with a numbered source list (URL / PMID / DOI and date). Plain, precise language, no filler. Return a 3-line summary of the report.`, { label: 'writer' })

// ---------- Review (+ Fix), at most two rounds ----------
let lastReview = null
let rounds = 0
for (let round = 1; round <= 2; round++) {
  phase('Review')
  const review = await agent(`You are an independent reviewer. You did not write this report. Read ${OUT}/report.md.
Question it answers: ${Q}. Today: ${DATE}.

Check: does it actually answer the question; are key numbers correct and current (spot-check the 5 most important against their sources with WebSearch/WebFetch); are facts, estimates and inferences labeled honestly; missing major considerations; internal contradictions; unsupported recommendations. Report concrete issues with fixes. Do not edit the file.`, { label: `review-${round}`, phase: 'Review', schema: REVIEW, model: 'opus', effort: 'high' })
  lastReview = review
  rounds = round
  if (!review.issues.length) break

  phase('Fix')
  await agent(`Revise ${OUT}/report.md to address these review findings: ${JSON.stringify(review.issues)}
Verify any number you change against its source. Keep the structure. At the end of the report, add or update a short "Review" section: reviewer = independent Claude Opus 5.5 (high effort), round ${round}, and the main changes made. Return a one-line summary of changes.`, { label: `fix-${round}`, phase: 'Fix' })

  if (!review.issues.some(i => i.severity === 'critical')) break
  log(`Round ${round} had critical issues; running a second review.`)
}

return {
  report: `${OUT}/report.md`,
  sub_questions: subs.length,
  researched: allFindings.length,
  failed_researchers: failed,
  gap_fill: gapResults.map(x => x.sub.id),
  review_rounds: rounds,
  review_verdict: lastReview && lastReview.verdict,
  review_issues: lastReview ? lastReview.issues.length : 0,
}
