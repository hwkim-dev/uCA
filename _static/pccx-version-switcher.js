(function () {
  "use strict";

  const ACTIVE_STATUSES = new Set(["current", "available", "archived"]);

  function currentScriptBase() {
    const script = document.currentScript;
    if (script && script.src) {
      return new URL(".", script.src);
    }
    const fallback = document.querySelector('script[src$="pccx-version-switcher.js"]');
    if (fallback && fallback.src) {
      return new URL(".", fallback.src);
    }
    return new URL("_static/", window.location.href);
  }

  function pageLanguage() {
    const lang = document.documentElement.getAttribute("lang") || "";
    if (lang.toLowerCase().startsWith("ko")) {
      return "ko";
    }
    const parts = window.location.pathname.split("/").filter(Boolean);
    if (parts[0] === "ko") {
      return "ko";
    }
    return "en";
  }

  function entryUrl(entry, lang) {
    if (entry.urls && typeof entry.urls === "object" && entry.urls[lang]) {
      return entry.urls[lang];
    }
    return entry.url || "";
  }

  function normalizePath(url) {
    try {
      const parsed = new URL(url, window.location.origin);
      let pathname = parsed.pathname || "/";
      if (!pathname.endsWith("/")) {
        pathname += "/";
      }
      return pathname;
    } catch (_error) {
      return "";
    }
  }

  function activeSlug(entries, lang) {
    const currentPath = normalizePath(window.location.pathname);
    const specific = entries.find((entry) => {
      if (entry.slug === "current") {
        return false;
      }
      const target = normalizePath(entryUrl(entry, lang));
      return target && (currentPath === target || currentPath.startsWith(target));
    });
    return specific ? specific.slug : "current";
  }

  function buildEntry(entry, lang, active) {
    const url = entryUrl(entry, lang);
    const clickable = url && ACTIVE_STATUSES.has(entry.status);
    const node = document.createElement(clickable ? "a" : "span");
    node.className = "pccx-version-switcher__entry";
    node.dataset.pccxVersion = entry.slug || entry.label || "";
    node.dataset.pccxVersionStatus = entry.status || "";
    node.textContent = entry.label || entry.slug || "Version";
    if (entry.slug === active) {
      node.classList.add("is-active");
      node.setAttribute("aria-current", "page");
    }
    if (clickable) {
      node.href = url;
      node.dataset.pccxVersionUrl = url;
    } else {
      node.classList.add("is-disabled");
      node.setAttribute("aria-disabled", "true");
    }
    return node;
  }

  function placeSwitcher(switcher) {
    const tree = document.querySelector(".sidebar-tree");
    if (!tree) {
      switcher.hidden = false;
      return;
    }
    const list = tree.querySelector(":scope > ul") || tree.querySelector("ul");
    const firstItem = list ? list.querySelector(":scope > li") || list.querySelector("li") : null;
    const wrapper = document.createElement("li");
    wrapper.className = "toctree-l1 pccx-version-switcher-item";
    wrapper.appendChild(switcher);
    if (firstItem && firstItem.parentNode) {
      firstItem.insertAdjacentElement("afterend", wrapper);
    } else if (list) {
      list.insertBefore(wrapper, list.firstChild);
    } else {
      tree.insertBefore(wrapper, tree.firstChild);
    }
    switcher.hidden = false;
  }

  function render(entries) {
    const switcher = document.querySelector("[data-pccx-version-switcher]");
    if (!switcher || !Array.isArray(entries) || entries.length === 0) {
      return;
    }
    const lang = pageLanguage();
    const active = activeSlug(entries, lang);
    const list = switcher.querySelector("[data-pccx-version-list]");
    if (!list) {
      return;
    }
    list.replaceChildren();
    for (const entry of entries) {
      if (!entry || !entry.label) {
        continue;
      }
      list.appendChild(buildEntry(entry, lang, active));
    }
    placeSwitcher(switcher);
  }

  async function main() {
    const base = currentScriptBase();
    const manifestUrl = new URL("pccx_versions.json", base);
    const response = await fetch(manifestUrl, { cache: "no-cache" });
    if (!response.ok) {
      throw new Error("version manifest unavailable");
    }
    render(await response.json());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", main, { once: true });
  } else {
    main();
  }
})();
