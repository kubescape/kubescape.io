/**
 * Kubescape Documentation Repository & Page Source Modal
 * Provides a professional, interactive modal connecting contributors directly
 * to the kubescape.io repository and the source file of the current page.
 */

(function () {
  function getPageSourceInfo() {
    const metaPath = document.querySelector('meta[name="doc-repo-path"]');
    const metaUrl = document.querySelector('meta[name="doc-github-url"]');

    let filePath = metaPath ? metaPath.getAttribute("content") : "";
    let githubUrl = metaUrl ? metaUrl.getAttribute("content") : "";

    // Fallback based on pathname if meta tag is missing
    if (!filePath) {
      let path = window.location.pathname.replace(/^\/|\/$/g, "");
      if (!path || path === "index.html") {
        filePath = "docs/index.md";
      } else {
        filePath = `docs/${path}.md`;
      }
      githubUrl = `https://github.com/kubescape/kubescape.io/blob/main/${filePath}`;
    }

    return { filePath, githubUrl };
  }

  function createModal() {
    if (document.getElementById("ks-repo-modal-root")) return;

    const modalRoot = document.createElement("div");
    modalRoot.id = "ks-repo-modal-root";
    modalRoot.className = "ks-repo-modal";
    modalRoot.setAttribute("role", "dialog");
    modalRoot.setAttribute("aria-modal", "true");
    modalRoot.setAttribute("aria-hidden", "true");

    modalRoot.innerHTML = `
      <div class="ks-repo-modal__backdrop" data-ks-modal-close></div>
      <div class="ks-repo-modal__dialog" role="document">
        <!-- Header -->
        <div class="ks-repo-modal__header">
          <div class="ks-repo-modal__title-group">
            <div class="ks-repo-modal__icon">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
                <path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2Z"/>
              </svg>
            </div>
            <div>
              <h3 class="ks-repo-modal__title">Documentation Repository</h3>
              <span class="ks-repo-modal__subtitle">github.com/kubescape/kubescape.io</span>
            </div>
          </div>
          <button type="button" class="ks-repo-modal__close-btn" data-ks-modal-close aria-label="Close dialog">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
        </div>

        <!-- Body -->
        <div class="ks-repo-modal__body">
          <!-- Section 1: Docs Repository -->
          <div class="ks-repo-modal__section">
            <p class="ks-repo-modal__desc">
              The documentation, tutorials, and website content for Kubescape are openly maintained in the <strong><code>kubescape.io</code></strong> repository.
            </p>
            <a href="https://github.com/kubescape/kubescape.io" target="_blank" rel="noopener noreferrer" class="ks-repo-modal__primary-btn">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                <path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2Z"/>
              </svg>
              <span>Open kubescape.io on GitHub</span>
              <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" class="ks-repo-modal__ext-icon">
                <path d="M14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3m-2 16H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7z"/>
              </svg>
            </a>
          </div>

          <!-- Section 2: Current Page Info -->
          <div class="ks-repo-modal__section ks-repo-modal__section--page">
            <span class="ks-repo-modal__section-label">Current Page Source</span>
            <div class="ks-repo-modal__path-box">
              <code class="ks-repo-modal__path-text" id="ks-repo-current-path">docs/index.md</code>
              <button type="button" class="ks-repo-modal__copy-btn" id="ks-repo-copy-path-btn" title="Copy repository path">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor">
                  <path d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"/>
                </svg>
                <span class="ks-repo-modal__copy-text">Copy</span>
              </button>
            </div>
            <a href="#" target="_blank" rel="noopener noreferrer" class="ks-repo-modal__secondary-link" id="ks-repo-view-file-btn">
              <svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
              <span>View this file on GitHub</span>
              <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor" class="ks-repo-modal__ext-icon">
                <path d="M14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3m-2 16H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7z"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- Footer Note -->
        <div class="ks-repo-modal__footer">
          <p>
            Looking for the CLI, engine, or runtime operator? Visit the
            <a href="https://github.com/kubescape/kubescape" target="_blank" rel="noopener noreferrer">kubescape/kubescape</a> repository.
          </p>
        </div>
      </div>
    `;

    document.body.appendChild(modalRoot);

    // Event listeners for close
    modalRoot.querySelectorAll("[data-ks-modal-close]").forEach(el => {
      el.addEventListener("click", closeModal);
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modalRoot.classList.contains("is-open")) {
        closeModal();
      }
    });

    // Copy path button listener
    const copyBtn = modalRoot.querySelector("#ks-repo-copy-path-btn");
    if (copyBtn) {
      copyBtn.addEventListener("click", async () => {
        const pathText = modalRoot.querySelector("#ks-repo-current-path").textContent;
        try {
          await navigator.clipboard.writeText(pathText);
          const copyLabel = copyBtn.querySelector(".ks-repo-modal__copy-text");
          const originalText = copyLabel.textContent;
          copyLabel.textContent = "Copied! ✓";
          copyBtn.classList.add("is-copied");
          setTimeout(() => {
            copyLabel.textContent = originalText;
            copyBtn.classList.remove("is-copied");
          }, 2000);
        } catch (err) {
          console.error("Failed to copy path:", err);
        }
      });
    }
  }

  function openModal() {
    createModal();
    const modalRoot = document.getElementById("ks-repo-modal-root");
    if (!modalRoot) return;

    // Refresh current page info
    const { filePath, githubUrl } = getPageSourceInfo();
    const pathElem = modalRoot.querySelector("#ks-repo-current-path");
    const viewFileBtn = modalRoot.querySelector("#ks-repo-view-file-btn");

    if (pathElem) pathElem.textContent = filePath;
    if (viewFileBtn) viewFileBtn.setAttribute("href", githubUrl);

    modalRoot.classList.add("is-open");
    modalRoot.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    const modalRoot = document.getElementById("ks-repo-modal-root");
    if (!modalRoot) return;

    modalRoot.classList.remove("is-open");
    modalRoot.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  function bindHeaderButton() {
    const headerBtn = document.querySelector("[data-ks-docs-repo-btn]");
    if (headerBtn) {
      headerBtn.addEventListener("click", openModal);
    }
  }

  function init() {
    createModal();
    bindHeaderButton();
  }

  document.addEventListener("DOMContentLoaded", init);
  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  }
})();

