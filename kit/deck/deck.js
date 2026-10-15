/* Falconshire kit: HTML slide deck navigation (2026-10). No dependencies.
   Keys: → ↓ PageDown Space next; ← ↑ PageUp Shift+Space previous; Home / End; O overview; Esc leaves overview.
   Click or tap the right / left half, or swipe on touch screens. #3 deep-links slide 3; each move is a
   history entry, so browser Back / Forward step between slides. Speaker notes: <aside class="k-notes"> (hidden). */
(function () {
  "use strict";
  function init() {
    var body = document.body, slides = [].slice.call(document.querySelectorAll(".k-slide"));
    if (!slides.length || body.classList.contains("k-deck--ready")) return;
    var zh = !/^en/i.test(document.documentElement.lang || ""), cur = 0, sx = null, sy = 0, swiped = 0;
    var icon = function (d) { return '<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6">' + d + "</svg>"; };
    var bar = document.createElement("nav");
    bar.className = "k-deck-bar";
    bar.setAttribute("aria-label", zh ? "幻灯片导航" : "Slides");
    bar.innerHTML =
      '<button type="button" class="k-deck-bar__btn" data-k-deck="prev" aria-label="' + (zh ? "上一张" : "Previous") + '">' + icon('<path d="M10 3 5 8l5 5"/>') + "</button>" +
      '<span class="k-deck-bar__count" aria-live="polite"></span>' +
      '<button type="button" class="k-deck-bar__btn" data-k-deck="next" aria-label="' + (zh ? "下一张" : "Next") + '">' + icon('<path d="m6 3 5 5-5 5"/>') + "</button>" +
      '<button type="button" class="k-deck-bar__btn" data-k-deck="overview" aria-pressed="false" aria-label="' + (zh ? "全部幻灯片" : "All slides") + '">' +
      icon('<rect x="2.5" y="2.5" width="4.5" height="4.5"/><rect x="9" y="2.5" width="4.5" height="4.5"/><rect x="2.5" y="9" width="4.5" height="4.5"/><rect x="9" y="9" width="4.5" height="4.5"/>') + "</button>";
    body.appendChild(bar);
    var count = bar.querySelector(".k-deck-bar__count"), btn = {};
    [].forEach.call(bar.querySelectorAll("button"), function (b) { btn[b.getAttribute("data-k-deck")] = b; });
    slides.forEach(function (s, i) {
      s.setAttribute("role", "group");
      s.setAttribute("aria-roledescription", zh ? "幻灯片" : "slide");
      s.setAttribute("aria-label", (i + 1) + " / " + slides.length);
    });

    function fromHash() {
      var m = /^#(\d+)$/.exec(location.hash);
      return m ? Math.min(Math.max(+m[1], 1), slides.length) - 1 : 0;
    }
    function overview() { return body.classList.contains("k-deck--overview"); }
    function zoomed() { return window.visualViewport && window.visualViewport.scale > 1.05; }
    function show(i, push) {
      cur = Math.max(0, Math.min(slides.length - 1, i));
      slides.forEach(function (s, k) { s.classList.toggle("is-active", k === cur); });
      count.textContent = (cur + 1) + " / " + slides.length;
      btn.prev.disabled = cur === 0;
      btn.next.disabled = cur === slides.length - 1;
      var h = "#" + (cur + 1);
      if (push && location.hash !== h) history.pushState(null, "", h);
    }
    function setOverview(on) {
      body.classList.toggle("k-deck--overview", on);
      btn.overview.setAttribute("aria-pressed", String(on));
      if (on) slides[cur].scrollIntoView({ block: "center", behavior: "instant" });
      else window.scrollTo(0, 0);
    }

    bar.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      var a = b.getAttribute("data-k-deck");
      if (a === "overview") setOverview(!overview());
      else show(cur + (a === "next" ? 1 : -1), true);
    });
    document.addEventListener("keydown", function (e) {
      var t = e.target, k = e.key;
      if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.altKey) return;
      if (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) return;
      if (k === "o" || k === "O") { setOverview(!overview()); e.preventDefault(); return; }
      if (overview()) { if (k === "Escape") { setOverview(false); e.preventDefault(); } return; }
      if ((k === " " || k === "Enter") && /^(BUTTON|A|SUMMARY)$/.test(t.tagName)) return;
      var d = { ArrowRight: 1, ArrowDown: 1, PageDown: 1, " ": 1, ArrowLeft: -1, ArrowUp: -1, PageUp: -1 }[k];
      if (k === " " && e.shiftKey) d = -1;
      if (k === "Home") show(0, true);
      else if (k === "End") show(slides.length - 1, true);
      else if (d) show(cur + d, true);
      else return;
      e.preventDefault();
    });
    document.addEventListener("click", function (e) {
      var t = e.target;
      if (Date.now() - swiped < 500 || zoomed()) return;
      if (t.closest("a,button,input,select,textarea,label,summary,video,audio,.k-deck-bar,[data-k-deck-noclick]")) return;
      if (overview()) {
        var s = t.closest(".k-slide");
        if (s) { show(slides.indexOf(s), true); setOverview(false); }
        return;
      }
      if (String(window.getSelection ? window.getSelection() : "")) return;
      show(cur + (e.clientX < window.innerWidth / 2 ? -1 : 1), true);
    });
    document.addEventListener("touchstart", function (e) {
      sx = e.touches.length === 1 ? e.touches[0].clientX : null;
      sy = e.touches.length === 1 ? e.touches[0].clientY : 0;
    }, { passive: true });
    document.addEventListener("touchend", function (e) {
      if (sx === null || overview() || zoomed()) return;
      var p = e.changedTouches[0], dx = p.clientX - sx, dy = p.clientY - sy;
      sx = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > 1.5 * Math.abs(dy)) { swiped = Date.now(); show(cur + (dx < 0 ? 1 : -1), true); }
    }, { passive: true });
    window.addEventListener("popstate", function () { show(fromHash(), false); });

    body.classList.add("k-deck--ready");
    show(fromHash(), false);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
