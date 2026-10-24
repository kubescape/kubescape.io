/* Keep Material's palette engine and storage, with a two-state button and
 * system following until the visitor makes an explicit choice. */
document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector("[data-theme-toggle]");
  const palette = document.querySelector('[data-md-component="palette"]');
  if (!button || !palette) return;

  const system = matchMedia("(prefers-color-scheme: dark)");
  let manual = __md_get("__palette_manual") === true;
  let transition;

  function updateLabel() {
    const dark = document.body.dataset.mdColorScheme === "slate";
    const label = dark ? "Switch to light mode" : "Switch to dark mode";
    button.setAttribute("aria-label", label);
    button.setAttribute("title", label);
  }

  function select(scheme) {
    // Restrict the color transition to a theme change so normal drawer/search
    // animations keep Material's own transition rules.
    if (document.body.classList.contains("theme-ready")) {
      clearTimeout(transition);
      document.body.classList.add("theme-transition");
      transition = setTimeout(() => {
        document.body.classList.remove("theme-transition");
      }, 200);
    }
    const input = palette.querySelector(`[data-md-color-scheme="${scheme}"]`);
    input.checked = true;
    input.dispatchEvent(new Event("change", { bubbles: true }));
    updateLabel();
  }

  button.addEventListener("click", () => {
    manual = true;
    __md_set("__palette_manual", true);
    select(document.body.dataset.mdColorScheme === "slate" ? "default" : "slate");
  });

  system.addEventListener("change", () => {
    if (!manual) select(system.matches ? "slate" : "default");
  });

  // Reconcile changes that happened while scripts were loading.
  if (!manual) select(system.matches ? "slate" : "default");
  updateLabel();
  button.hidden = false;
  requestAnimationFrame(() => {
    document.body.classList.add("theme-ready");
  });
});
