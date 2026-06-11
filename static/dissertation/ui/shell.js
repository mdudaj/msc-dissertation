(function () {
  const storageKey = "kisomo.sidebarCollapsed";

  function applyState(shell, collapsed) {
    shell.classList.toggle("kisomo-shell--collapsed", collapsed);
    const toggle = shell.querySelector("[data-kisomo-drawer-toggle]");
    if (toggle) {
      toggle.setAttribute("aria-expanded", collapsed ? "false" : "true");
      toggle.setAttribute(
        "aria-label",
        collapsed ? "Expand side navigation" : "Minimize side navigation",
      );
    }
  }

  function initShell() {
    const shell = document.querySelector(".kisomo-shell");
    if (!shell) {
      return;
    }
    const collapsed = window.localStorage.getItem(storageKey) === "true";
    applyState(shell, collapsed);

    const toggle = shell.querySelector("[data-kisomo-drawer-toggle]");
    if (!toggle) {
      return;
    }
    toggle.addEventListener("click", function () {
      const next = !shell.classList.contains("kisomo-shell--collapsed");
      window.localStorage.setItem(storageKey, String(next));
      applyState(shell, next);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initShell);
  } else {
    initShell();
  }
})();
