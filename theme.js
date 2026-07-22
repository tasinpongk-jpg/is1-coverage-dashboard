/**
 * Shared appearance runtime for the IS1 Terminal.
 * Applies the saved theme before body paint, then installs controls and motion.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "is1_theme";
  var MODES = ["system", "light", "dark"];
  var LABELS = {
    system:["A", "theme.system", "Follow system theme"],
    light:["☼", "theme.light", "Use light theme"],
    dark:["◐", "theme.dark", "Use dark theme"],
  };
  var root = document.documentElement;
  var systemDark = window.matchMedia("(prefers-color-scheme: dark)");
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function savedMode() {
    try {
      var mode = localStorage.getItem(STORAGE_KEY);
      return MODES.indexOf(mode) >= 0 ? mode : "system";
    } catch (e) {
      return "system";
    }
  }

  function effectiveTheme(mode) {
    return mode === "system" ? (systemDark.matches ? "dark" : "light") : mode;
  }

  var currentMode = savedMode();

  function apply(mode, persist) {
    currentMode = MODES.indexOf(mode) >= 0 ? mode : "system";
    root.dataset.themeMode = currentMode;
    root.dataset.theme = effectiveTheme(currentMode);
    if (persist) {
      try { localStorage.setItem(STORAGE_KEY, currentMode); } catch (e) {}
    }
    updateControls();
    window.dispatchEvent(new CustomEvent("themechange", {
      detail: { mode:currentMode, theme:root.dataset.theme },
    }));
  }

  function setMode(mode) {
    var change = function () { apply(mode, true); };
    root.classList.add("theme-changing");
    if (document.startViewTransition && !reducedMotion.matches) {
      document.startViewTransition(change).finished.finally(function () {
        root.classList.remove("theme-changing");
      });
    } else {
      change();
      window.setTimeout(function () { root.classList.remove("theme-changing"); }, 280);
    }
  }

  apply(currentMode, false);

  function updateControls() {
    document.querySelectorAll(".theme-switch button").forEach(function (button) {
      var active = button.dataset.themeValue === currentMode;
      var label = (window.I18N && I18N.t) ? I18N.t(LABELS[button.dataset.themeValue][1]) : LABELS[button.dataset.themeValue][2];
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
      button.setAttribute("aria-label", label);
      button.title = label;
    });
  }

  function themeControl() {
    var control = document.createElement("div");
    control.className = "theme-switch";
    control.setAttribute("role", "group");
    control.setAttribute("aria-label", "Color theme");
    MODES.forEach(function (mode) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "theme-" + (mode === "system" ? "auto" : mode === "light" ? "sun" : "moon");
      button.dataset.themeValue = mode;
      button.textContent = LABELS[mode][0];
      button.addEventListener("click", function () { setMode(mode); });
      control.appendChild(button);
    });
    return control;
  }

  function placeControl() {
    if (document.querySelector(".theme-switch")) return;
    var control = themeControl();
    var header = document.querySelector(".is1s-topbar") || document.querySelector(".gtopbar") || document.querySelector("header");
    if (!header) {
      control.classList.add("theme-floating");
      document.body.appendChild(control);
      updateControls();
      return;
    }
    var shellControls = header.querySelector(".is1s-controls");
    var language = header.querySelector(".i18n-toggle,.langtoggle");
    if (shellControls) shellControls.appendChild(control);
    else if (language) language.insertAdjacentElement("afterend", control);
    else header.appendChild(control);
    updateControls();
  }

  var revealSelector = [
    ".phbanner",
    "main > .today-bar",
    "main > .ai-take",
    ".sec-title",
    ".group-title",
    ".dash-card",
    ".agent-card",
    ".rm-card",
    ".hstat",
    ".kpi",
    ".metric-section",
    ".icard",
    ".alert-card",
    ".filing",
    ".item",
    ".table-wrap",
    ".ticker-banner",
    "details.fold",
    ".is1s-page-head",
    ".is1-home-control",
    ".is1-home-panel",
  ].join(",");

  var revealObserver = null;
  var motionStarted = false;
  if ("IntersectionObserver" in window && !reducedMotion.matches) {
    revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-revealed");
        revealObserver.unobserve(entry.target);
      });
    }, { rootMargin:"0px 0px -5% 0px", threshold:0.04 });
  }

  function registerMotion(scope) {
    var nodes = [];
    if (scope.nodeType === 1 && scope.matches(revealSelector)) nodes.push(scope);
    if (scope.querySelectorAll) nodes = nodes.concat(Array.from(scope.querySelectorAll(revealSelector)));
    nodes.forEach(function (node, index) {
      if (node.classList.contains("motion-reveal")) return;
      node.classList.add("motion-reveal");
      node.style.setProperty("--motion-order", String(index % 8));
      if (revealObserver && motionStarted) revealObserver.observe(node);
      else if (!revealObserver) node.classList.add("is-revealed");
    });
  }

  function startMotion() {
    registerMotion(document);
    requestAnimationFrame(function () {
      root.classList.add("motion-ready");
      requestAnimationFrame(function () {
        motionStarted = true;
        document.querySelectorAll(".motion-reveal").forEach(function (node) {
          var rect = node.getBoundingClientRect();
          if (rect.top < innerHeight * .95 && rect.bottom > 0) node.classList.add("is-revealed");
          else if (revealObserver) revealObserver.observe(node);
        });
      });
    });
    new MutationObserver(function (records) {
      records.forEach(function (record) {
        record.addedNodes.forEach(function (node) {
          if (node.nodeType === 1) registerMotion(node);
        });
      });
    }).observe(document.body, { childList:true, subtree:true });
  }

  function ready() {
    placeControl();
    startMotion();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ready);
  else ready();

  systemDark.addEventListener("change", function () {
    if (currentMode === "system") apply("system", false);
  });
  window.addEventListener("i18n:change", updateControls);

  window.IS1Theme = {
    getMode:function () { return currentMode; },
    getTheme:function () { return root.dataset.theme; },
    setMode:setMode,
  };
})();
