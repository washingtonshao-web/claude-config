/* Falconshire design kit v1 behaviours: theme toggle, drawers, chips, tabs, TOC highlight.
   Markup hooks only (data-k-*); pages add their own logic on top. */
(function () {
  var root = document.documentElement;
  var KEY = "k-theme";
  try { var saved = localStorage.getItem(KEY); if (saved) root.setAttribute("data-theme", saved); } catch (e) {}

  function isDark() {
    var t = root.getAttribute("data-theme");
    return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function paintToggles() {
    document.querySelectorAll("[data-k-theme-toggle]").forEach(function (b) {
      b.textContent = isDark() ? "☀" : "☾";
      b.setAttribute("aria-label", isDark() ? "切换到浅色" : "切换到深色");
    });
  }

  function openDrawer(id) {
    var d = document.getElementById(id); if (!d) return;
    var scrim = document.querySelector(".k-scrim");
    d.setAttribute("data-open", "true"); d.setAttribute("aria-hidden", "false");
    if (scrim) scrim.setAttribute("data-open", "true");
    document.body.style.overflow = "hidden";
    var c = d.querySelector("[data-k-close]"); if (c) c.focus();
  }
  function closeDrawers() {
    document.querySelectorAll(".k-drawer[data-open='true']").forEach(function (d) {
      d.setAttribute("data-open", "false"); d.setAttribute("aria-hidden", "true");
    });
    var scrim = document.querySelector(".k-scrim");
    if (scrim) scrim.setAttribute("data-open", "false");
    document.body.style.overflow = "";
  }
  window.kit = { openDrawer: openDrawer, closeDrawers: closeDrawers };

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-k-theme-toggle],[data-k-open],[data-k-close],.k-scrim,.k-chip,.k-tab");
    if (!t) return;
    if (t.hasAttribute("data-k-theme-toggle")) {
      var next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem(KEY, next); } catch (err) {}
      paintToggles();
    } else if (t.hasAttribute("data-k-open")) {
      openDrawer(t.getAttribute("data-k-open"));
    } else if (t.hasAttribute("data-k-close") || t.classList.contains("k-scrim")) {
      closeDrawers();
    } else if (t.classList.contains("k-chip")) {
      var group = t.closest("[data-k-single]");
      if (group) group.querySelectorAll(".k-chip").forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
      t.setAttribute("aria-pressed", group ? "true" : String(t.getAttribute("aria-pressed") !== "true"));
      t.dispatchEvent(new CustomEvent("k:chip", { bubbles: true }));
    } else if (t.classList.contains("k-tab")) {
      var list = t.closest(".k-tabs");
      list.querySelectorAll(".k-tab").forEach(function (b) {
        var on = b === t; b.setAttribute("aria-selected", String(on));
        var p = document.getElementById(b.getAttribute("aria-controls")); if (p) p.hidden = !on;
      });
    }
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeDrawers(); });

  function tocSpy() {
    var links = document.querySelectorAll(".k-toc a[href^='#']");
    if (!links.length || !("IntersectionObserver" in window)) return;
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.removeAttribute("aria-current"); });
        var a = map[en.target.id]; if (a) a.setAttribute("aria-current", "true");
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { paintToggles(); tocSpy(); });
  else { paintToggles(); tocSpy(); }
})();
