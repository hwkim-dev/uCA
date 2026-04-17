/**
 * mermaid-theme.js
 * Re-renders Mermaid diagrams whenever PyData Sphinx Theme switches
 * between light and dark mode (it toggles data-theme on <html>).
 *
 * sphinxcontrib-mermaid renders diagrams as <pre class="mermaid"> elements
 * containing the source text. When we want a different theme we must:
 *   1. Swap the SVG out and restore the raw source text into the <pre>.
 *   2. Re-run mermaid.run() with the new theme configuration.
 */

(function () {
  "use strict";

  function getCurrentTheme() {
    return document.documentElement.getAttribute("data-theme") === "dark"
      ? "dark"
      : "default";
  }

  function getMermaidConfig(theme) {
    return {
      startOnLoad: false,
      securityLevel: "loose",
      theme: theme,
      flowchart: {
        htmlLabels: true,
        curve: "basis",
        useMaxWidth: false,
        padding: 12,
      },
      sequence: {
        useMaxWidth: false,
        mirrorActors: false,
      },
    };
  }

  /**
   * Store the original Mermaid source for each <pre class="mermaid"> so we
   * can restore it before re-rendering (Mermaid replaces the element with
   * an <svg> and the source is lost after the first render).
   */
  function cacheSources() {
    document.querySelectorAll("pre.mermaid").forEach(function (el) {
      if (!el.dataset.mermaidSrc) {
        el.dataset.mermaidSrc = el.textContent;
      }
    });
  }

  /**
   * Reset each Mermaid container back to its raw source so Mermaid can
   * re-render it with the new theme.
   */
  function resetDiagrams() {
    document.querySelectorAll("pre.mermaid").forEach(function (el) {
      if (el.dataset.mermaidSrc) {
        el.removeAttribute("data-processed");
        el.innerHTML = el.dataset.mermaidSrc;
      }
    });
  }

  function renderWithTheme(theme) {
    if (typeof window.mermaid === "undefined") return;
    resetDiagrams();
    window.mermaid.initialize(getMermaidConfig(theme));
    window.mermaid.run({
      querySelector: "pre.mermaid",
    });
  }

  function init() {
    if (typeof window.mermaid === "undefined") return;

    cacheSources();
    var theme = getCurrentTheme();
    window.mermaid.initialize(getMermaidConfig(theme));
    window.mermaid.run({ querySelector: "pre.mermaid" });

    /* Watch for PyData theme switching: it sets data-theme on <html>. */
    var observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (m) {
        if (m.attributeName === "data-theme") {
          renderWithTheme(getCurrentTheme());
        }
      });
    });
    observer.observe(document.documentElement, { attributes: true });
  }

  /* Mermaid is loaded asynchronously by sphinxcontrib-mermaid.
   * Wait until it's available before initialising. */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      /* Give Mermaid script a tick to finish loading. */
      setTimeout(init, 0);
    });
  } else {
    setTimeout(init, 0);
  }
})();
