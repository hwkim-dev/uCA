// pccx — Korean auto-translate banner: dismiss + persist.
//
// Adds an X close button and a "Don't show again" checkbox to the
// Furo announcement bar on Korean pages. Dismiss state lives in
// localStorage under a versioned key so a future banner copy
// rollover can re-introduce the notice without colliding with old
// dismiss state.
//
// Path-scoped to /ko/ so the banner controls never appear on the
// English tree even if the announcement slot is non-empty.

(function () {
    "use strict";

    if (window.location.pathname.indexOf("/ko/") === -1) {
        return;
    }

    var STORAGE_KEY = "pccx-auto-translate-banner-hidden-v1";

    function readDismissed() {
        try {
            return window.localStorage &&
                localStorage.getItem(STORAGE_KEY) === "1";
        } catch (e) {
            return false;
        }
    }

    function writeDismissed() {
        try {
            window.localStorage &&
                localStorage.setItem(STORAGE_KEY, "1");
        } catch (e) {
            // localStorage can be unavailable in private-browsing
            // contexts; the banner just falls back to one-time
            // dismiss in that session.
        }
    }

    if (readDismissed()) {
        // Hide before first paint to avoid a flash of the banner.
        var hideStyle = document.createElement("style");
        hideStyle.textContent =
            ".announcement { display: none !important; }";
        document.head.appendChild(hideStyle);
        return;
    }

    document.addEventListener("DOMContentLoaded", function () {
        var bar = document.querySelector(".announcement");
        if (!bar) {
            return;
        }

        var inner = bar.querySelector(".announcement-content") || bar;

        var label = document.createElement("label");
        label.className = "pccx-banner-dont-show";
        var checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        var labelText = document.createElement("span");
        labelText.textContent = "Don't show again · 다시 보지 않기";
        label.appendChild(checkbox);
        label.appendChild(labelText);

        checkbox.addEventListener("change", function () {
            if (checkbox.checked) {
                writeDismissed();
                bar.style.display = "none";
            }
        });

        var closeBtn = document.createElement("button");
        closeBtn.type = "button";
        closeBtn.className = "pccx-banner-close";
        closeBtn.setAttribute(
            "aria-label",
            "Dismiss this banner · 이 배너 닫기"
        );
        closeBtn.textContent = "✕";

        closeBtn.addEventListener("click", function () {
            bar.style.display = "none";
        });

        inner.appendChild(label);
        inner.appendChild(closeBtn);
    });
})();
