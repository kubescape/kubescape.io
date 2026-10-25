/* Keep Material's palette engine and storage, with a two-state button and
 * system following until the visitor makes an explicit choice. */
document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector("[data-theme-toggle]");
  const palette = document.querySelector('[data-md-component="palette"]');
  if (!button || !palette) return;

  const system = matchMedia("(prefers-color-scheme: dark)");
  let revealing = false;

  function updateLabel() {
    const dark = document.body.dataset.mdColorScheme === "slate";
    const label = dark ? "Switch to light mode" : "Switch to dark mode";
    button.setAttribute("aria-label", label);
    button.setAttribute("title", label);
  }

  function select(scheme) {
    const input = palette.querySelector(`[data-md-color-scheme="${scheme}"]`);
    input.checked = true;
    input.dispatchEvent(new Event("change", { bubbles: true }));
    updateLabel();
  }

  button.addEventListener("click", async () => {
    if (revealing) return;
    __md_set("__palette_manual", true);
    const scheme = document.body.dataset.mdColorScheme === "slate" ? "default" : "slate";
    if (!document.startViewTransition || matchMedia("(prefers-reduced-motion: reduce)").matches) {
      select(scheme);
      return;
    }

    const { left, top, width, height } = button.getBoundingClientRect();
    const x = left + width / 2;
    const y = top + height / 2;
    const radius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    const root = document.documentElement;
    revealing = true;
    root.classList.add("theme-reveal");
    try {
      const transition = document.startViewTransition(() => select(scheme));
      transition.ready.then(() => {
        root.animate({
          clipPath: [`circle(0px at ${x}px ${y}px)`, `circle(${radius}px at ${x}px ${y}px)`]
        }, {
          duration: 450,
          // Respond immediately, then gently decelerate without a mid-reveal rush.
          easing: "cubic-bezier(0.22, 0.61, 0.36, 1)",
          pseudoElement: "::view-transition-new(root)"
        });
      }).catch(() => transition.skipTransition());
      await transition.finished;
    } catch {
      // A skipped or unavailable snapshot must never prevent changing theme.
      select(scheme);
    } finally {
      root.classList.remove("theme-reveal");
      revealing = false;
    }
  });

  system.addEventListener("change", () => {
    if (__md_get("__palette_manual") !== true) select(system.matches ? "slate" : "default");
  });

  // Reconcile changes that happened while scripts were loading.
  if (__md_get("__palette_manual") !== true) select(system.matches ? "slate" : "default");
  updateLabel();
  button.hidden = false;
});
