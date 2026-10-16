# Design in Codex

The rules in this skill are the same for Claude and Codex. Only these steps change, because they name Claude tools.

| Claude step | In Codex |
|---|---|
| Publish an Artifact (`artifact.md`) | No Artifacts. A page someone will open goes out through the Falconshire Publisher (`publish_static_site` on the falconshire-publisher MCP) or `E:\Claude\sites\publish.py`; a page only I look at is a local HTML file. Build it with the kit and `apply_kit.py` exactly as `artifact.md` says. |
| artifact-design skill | Not in Codex. Its contract that matters off claude.ai: a 2–4 word `<title>`, an explicit `body` background, no horizontal scroll at 375 px, 16px side gutter. The kit already meets the rest. |
| dataviz skill (chart method) | Not in Codex. `charts.md` alone is enough: conclusion title, 1–2 annotated notes, bars from zero, one value axis, source line. |
| Images through the codex-gpt skill (`images.md`) | Use Codex's own image generation with the same prompt template, saving into the project. |
| Astra scores the review (`review.md` §5) | Codex is the GPT side, so the independent scorer is Claude: run the independent-review skill (Claude Opus 5.5, high) with the screenshots, the scorecard and the Restraint and Avoid lists. If Claude is unavailable, use a fresh Codex sub-agent and label it 同模型复核. |
| design_guard hook | Claude-only reminder; Codex loads this skill from AGENTS.md instead. Nothing to run. |

Paths: `shoot.py` and `tokens.py` run the same from `~/.codex/skills/design/scripts/`. Put screenshots and scratch files in `E:\AI\Codex\temp`.
