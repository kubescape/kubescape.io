// Kubescape Control Explorer: Live filter and search across IDs and titles
document.addEventListener("DOMContentLoaded", function () {
  const explorer = document.getElementById("ks-control-explorer");
  if (!explorer) return;

  const searchInput = document.getElementById("ks-control-search");
  const clearBtn = document.getElementById("ks-search-clear");
  const countEl = document.getElementById("ks-controls-count");
  const noResultsEl = document.getElementById("ks-no-results");
  const resetBtn = document.getElementById("ks-reset-filters");
  const sevFilters = document.querySelectorAll("#ks-severity-filters .ks-pill");
  const catFilters = document.querySelectorAll("#ks-category-filters .ks-pill");
  const cards = Array.from(document.querySelectorAll(".ks-control-card"));

  let activeSev = "all";
  let activeCat = "all";
  let searchQuery = "";

  function updateView() {
    let visibleCount = 0;
    const query = searchQuery.trim().toLowerCase();

    cards.forEach((card) => {
      const id = (card.getAttribute("data-id") || "").toLowerCase();
      const sev = (card.getAttribute("data-sev") || "").toLowerCase();
      const cat = (card.getAttribute("data-cat") || "").toLowerCase();
      const title = (card.querySelector(".ks-card-title")?.textContent || "").toLowerCase();

      const matchesSev = activeSev === "all" || sev === activeSev;
      const matchesCat = activeCat === "all" || cat === activeCat;
      const matchesSearch = !query || id.includes(query) || title.includes(query);

      if (matchesSev && matchesCat && matchesSearch) {
        card.style.display = "";
        visibleCount++;
      } else {
        card.style.display = "none";
      }
    });

    if (countEl) {
      countEl.textContent = `Showing ${visibleCount} of ${cards.length} controls`;
    }

    if (noResultsEl) {
      noResultsEl.style.display = visibleCount === 0 ? "block" : "none";
    }

    if (clearBtn) {
      clearBtn.style.display = query.length > 0 ? "inline-flex" : "none";
    }
  }

  // Keyboard shortcut: Press "/" to focus search
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== searchInput && !["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName)) {
      e.preventDefault();
      searchInput?.focus();
      searchInput?.select();
    }
    if (e.key === "Escape" && document.activeElement === searchInput) {
      searchInput.value = "";
      searchQuery = "";
      updateView();
      searchInput.blur();
    }
  });

  searchInput?.addEventListener("input", function (e) {
    searchQuery = e.target.value;
    updateView();
  });

  clearBtn?.addEventListener("click", function () {
    if (searchInput) {
      searchInput.value = "";
      searchQuery = "";
      updateView();
      searchInput.focus();
    }
  });

  sevFilters.forEach((btn) => {
    btn.addEventListener("click", function () {
      sevFilters.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeSev = btn.getAttribute("data-filter") || "all";
      updateView();
    });
  });

  catFilters.forEach((btn) => {
    btn.addEventListener("click", function () {
      catFilters.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeCat = btn.getAttribute("data-cat") || "all";
      updateView();
    });
  });

  resetBtn?.addEventListener("click", function () {
    if (searchInput) searchInput.value = "";
    searchQuery = "";
    activeSev = "all";
    activeCat = "all";
    sevFilters.forEach((b) => b.classList.toggle("active", b.getAttribute("data-filter") === "all"));
    catFilters.forEach((b) => b.classList.toggle("active", b.getAttribute("data-cat") === "all"));
    updateView();
    searchInput?.focus();
  });

  function showCopiedFeedback(btn) {
    const originalText = btn.innerHTML;
    btn.innerHTML = "✓ Copied!";
    btn.classList.add("copied");
    setTimeout(() => {
      btn.innerHTML = originalText;
      btn.classList.remove("copied");
    }, 1800);
  }

  function fallbackCopyText(text, btn) {
    try {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      const success = document.execCommand("copy");
      document.body.removeChild(textarea);
      if (success) {
        showCopiedFeedback(btn);
      }
    } catch (err) {
      console.warn("Fallback copy failed:", err);
    }
  }

  // Copy command button
  document.querySelectorAll(".ks-copy-cmd-btn").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      const cmd = btn.getAttribute("data-cmd");
      if (!cmd) return;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(cmd)
          .then(() => {
            showCopiedFeedback(btn);
          })
          .catch((err) => {
            console.warn("navigator.clipboard.writeText failed, using fallback:", err);
            fallbackCopyText(cmd, btn);
          });
      } else {
        fallbackCopyText(cmd, btn);
      }
    });
  });

  // Initial render
  updateView();
});
