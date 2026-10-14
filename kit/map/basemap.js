/* Falconshire vector basemap loader (no dependencies).
   K.basemap(el, {center, zoom, bounds, dark, interactive, controls, maxZoom, base, options}) -> Promise<maplibregl.Map>
   Loads MapLibre GL + PMTiles from tiles.falconshire.com once, registers pmtiles://, and resolves
   with the map after its style has loaded (add your own sources/layers then). See README.md. */
(function () {
  var TILES = "https://tiles.falconshire.com";
  var LIB = {
    css: "/lib/maplibre-gl@5.24.0/maplibre-gl.css",
    js: "/lib/maplibre-gl@5.24.0/maplibre-gl.js",
    pm: "/lib/pmtiles@4.4.1/pmtiles.js"
  };
  var CJK_FONT = '"PingFang SC","Microsoft YaHei UI","Noto Sans SC",sans-serif';
  var loads = {}, ready = null;

  function inject(url, isCss) {
    return new Promise(function (ok, fail) {
      var n = document.createElement(isCss ? "link" : "script");
      if (isCss) { n.rel = "stylesheet"; n.href = url; } else { n.src = url; n.async = false; }
      n.onload = ok;
      n.onerror = function () { n.remove(); fail(new Error("basemap: failed to load " + url)); };
      document.head.appendChild(n);
    });
  }
  function load(url, isCss) { // one retry for flaky mobile links
    if (!loads[url]) loads[url] = inject(url, isCss).catch(function () {
      return new Promise(function (r) { setTimeout(r, 800); }).then(function () { return inject(url, isCss); });
    }).catch(function (e) { delete loads[url]; throw e; });
    return loads[url];
  }

  var proto = null;
  function libs(base) {
    if (!ready) ready = Promise.all([load(base + LIB.css, true), load(base + LIB.js), load(base + LIB.pm)])
      .then(function () {
        proto = new window.pmtiles.Protocol();
        window.maplibregl.addProtocol("pmtiles", proto.tile);
      })
      .catch(function (e) { ready = null; throw e; });
    return ready;
  }

  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function retry(fn, isAbort) { // one retry after 700 ms, never for aborted requests
    return fn().catch(function (e) {
      if (isAbort && isAbort(e)) throw e;
      return wait(700).then(fn);
    });
  }
  // PMTiles byte source with one retry per range request (mobile links drop requests).
  function retrySource(url) {
    var fs = new window.pmtiles.FetchSource(url);
    return {
      getKey: function () { return url; },
      getBytes: function (off, len, signal, etag) {
        return retry(function () { return fs.getBytes(off, len, signal, etag); }, function (e) {
          return (signal && signal.aborted) || (e && e.name === "AbortError") || e instanceof window.pmtiles.EtagMismatch;
        });
      }
    };
  }
  function loadStyle(url) {
    return retry(function () {
      return fetch(url).then(function (r) { if (!r.ok) throw new Error("basemap: style " + r.status); return r.json(); });
    }).then(function (style) {
      for (var k in style.sources) {
        var u = style.sources[k].url;
        if (u && u.indexOf("pmtiles://") === 0 && !proto.get(u.slice(10))) proto.add(new window.pmtiles.PMTiles(retrySource(u.slice(10))));
      }
      return style;
    });
  }

  var CSS = ".k-basemap .maplibregl-ctrl-attrib{font:11px/1.4 -apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei UI',sans-serif}" +
    "@media (pointer:coarse){.k-basemap .maplibregl-ctrl-group button{width:44px;height:44px}}" +
    ".k-basemap-dark .maplibregl-ctrl-group{background:#17181b;box-shadow:0 0 0 1px #2a2c31}" +
    ".k-basemap-dark .maplibregl-ctrl-group button+button{border-top-color:#2a2c31}" +
    ".k-basemap-dark .maplibregl-ctrl-icon{filter:invert(1)}" +
    ".k-basemap-dark .maplibregl-ctrl-attrib,.k-basemap-dark .maplibregl-ctrl-attrib.maplibregl-compact{background:rgba(15,16,18,.72);color:#c9d0da}" +
    ".k-basemap-dark .maplibregl-ctrl-attrib a{color:#c9d0da}" +
    ".k-basemap-dark .maplibregl-ctrl-attrib-button{filter:invert(1)}";
  function addCss() {
    if (document.getElementById("k-basemap-css")) return;
    var st = document.createElement("style");
    st.id = "k-basemap-css"; st.textContent = CSS;
    document.head.appendChild(st);
  }

  function prefersDark() {
    var t = document.documentElement.getAttribute("data-theme");
    if (t) return t === "dark";
    return !!(window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches);
  }

  function basemap(el, opts) {
    opts = opts || {};
    if (typeof el === "string") el = document.querySelector(el);
    if (!el) return Promise.reject(new Error("basemap: container not found"));
    var base = (opts.base || TILES).replace(/\/$/, "");
    var dark = opts.dark == null || opts.dark === "auto" ? prefersDark() : !!opts.dark;
    var coarse = !!(window.matchMedia && matchMedia("(pointer: coarse)").matches);
    // CJK glyphs are drawn locally; zh-CN picks Simplified glyph forms.
    if (!el.lang && !document.documentElement.lang) el.lang = "zh-CN";
    addCss();
    el.classList.add("k-basemap");
    el.classList.toggle("k-basemap-dark", dark);
    if (!el.style.background) el.style.background = dark ? "#0e1723" : "#c9d6df"; // water tone while tiles load

    return libs(base).then(function () {
      return loadStyle(base + "/v1/style/" + (dark ? "dark" : "light") + ".json");
    }).then(function (style) {
      var o = {
        container: el,
        style: style,
        center: opts.center || [105, 35],
        zoom: opts.zoom == null ? 3.4 : opts.zoom,
        maxZoom: opts.maxZoom || 16,
        interactive: opts.interactive !== false,
        cooperativeGestures: coarse && opts.interactive !== false,
        attributionControl: { compact: true },
        localIdeographFontFamily: CJK_FONT,
        dragRotate: false,
        pitchWithRotate: false,
        locale: {
          "CooperativeGesturesHandler.WindowsHelpText": "按住 Ctrl 并滚动鼠标以缩放地图",
          "CooperativeGesturesHandler.MacHelpText": "按住 ⌘ 并滚动以缩放地图",
          "CooperativeGesturesHandler.MobileHelpText": "用两根手指移动地图",
          "NavigationControl.ZoomIn": "放大",
          "NavigationControl.ZoomOut": "缩小"
        }
      };
      if (base !== TILES) {
        // local testing: serve style, fonts, sprites, geo from `base`; archives stay on the tiles host
        o.transformRequest = function (url) {
          if (url.indexOf(TILES + "/v1/") === 0 && !/\.pmtiles$/.test(url)) return { url: base + url.slice(TILES.length) };
        };
      }
      if (opts.bounds) { o.bounds = opts.bounds; o.fitBoundsOptions = { padding: 20 }; }
      var extra = opts.options || {};
      for (var k in extra) o[k] = extra[k];
      var map = new window.maplibregl.Map(o);
      if (opts.controls !== false && o.interactive) {
        map.addControl(new window.maplibregl.NavigationControl({ showCompass: false }), "top-right");
      }
      map.touchZoomRotate && map.touchZoomRotate.disableRotation();
      return new Promise(function (ok) {
        if (map.loaded()) ok(map); else map.once("load", function () { ok(map); });
      });
    });
  }

  basemap.styleURL = function (dark, base) { return (base || TILES) + "/v1/style/" + (dark ? "dark" : "light") + ".json"; };
  window.K = window.K || {};
  window.K.basemap = basemap;
})();
