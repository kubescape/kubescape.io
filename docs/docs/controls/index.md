# Control library

Explore and filter all Kubescape controls by identifier, keyword, category, or severity.

<div class="ks-control-explorer" id="ks-control-explorer">
  <div class="ks-explorer-search-bar">
    <span class="ks-search-icon" aria-hidden="true">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
    </span>
    <input type="text" id="ks-control-search" placeholder="Search controls (e.g. root, RBAC, C-0013, secret, memory)..." autocomplete="off" spellcheck="false" aria-label="Search controls">
    <button type="button" id="ks-search-clear" class="ks-search-clear" aria-label="Clear search" style="display:none;">✕</button>
    <kbd class="ks-search-kbd">/</kbd>
  </div>
  <div class="ks-filter-group">
    <span class="ks-filter-label">Severity:</span>
    <div class="ks-filter-pills" id="ks-severity-filters">
      <button type="button" class="ks-pill active" data-filter="all">All</button>
      <button type="button" class="ks-pill ks-pill-critical" data-filter="critical"><span class="ks-dot ks-dot-critical"></span>Critical</button>
      <button type="button" class="ks-pill ks-pill-high" data-filter="high"><span class="ks-dot ks-dot-high"></span>High</button>
      <button type="button" class="ks-pill ks-pill-medium" data-filter="medium"><span class="ks-dot ks-dot-medium"></span>Medium</button>
      <button type="button" class="ks-pill ks-pill-low" data-filter="low"><span class="ks-dot ks-dot-low"></span>Low</button>
    </div>
  </div>
  <div class="ks-filter-group">
    <span class="ks-filter-label">Category:</span>
    <div class="ks-filter-pills" id="ks-category-filters">
      <button type="button" class="ks-pill active" data-cat="all">All</button>
      <button type="button" class="ks-pill" data-cat="container">Containers & Pods</button>
      <button type="button" class="ks-pill" data-cat="rbac">RBAC & Secrets</button>
      <button type="button" class="ks-pill" data-cat="network">Network & Ingress</button>
      <button type="button" class="ks-pill" data-cat="cluster">Cluster & Control Plane</button>
    </div>
  </div>
  <div class="ks-explorer-status">
    <span id="ks-controls-count">Loading controls...</span>
  </div>
</div>

<div class="ks-controls-grid" id="ks-controls-grid">

  <div class="ks-control-card" data-id="C-0001" data-sev="high" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0001/">C-0001</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0001/">Forbidden Container Registries</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0001" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0002" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0002/">C-0002</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0002/">Prevent containers from allowing command execution</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0002" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0004" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0004/">C-0004</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0004/">Resources memory limit and request</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0004" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0005" data-sev="critical" data-cat="network">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0005/">C-0005</a>
      <span class="ks-badge ks-badge-critical">Critical</span>
    </div>
    <a class="ks-card-title" href="c-0005/">API server insecure port is enabled</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0005" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0007" data-sev="medium" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0007/">C-0007</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0007/">Roles with delete capabilities</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0007" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0009" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0009/">C-0009</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0009/">C-0009</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0009" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0012" data-sev="high" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0012/">C-0012</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0012/">Applications credentials in configuration files</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0012" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0013" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0013/">C-0013</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0013/">C-0013</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0013" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0014" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0014/">C-0014</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0014/">C-0014</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0014" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0015" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0015/">C-0015</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0015/">C-0015</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0015" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0016" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0016/">C-0016</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0016/">C-0016</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0016" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0017" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0017/">C-0017</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0017/">C-0017</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0017" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0018" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0018/">C-0018</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0018/">Configured readiness probe</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0018" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0020" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0020/">C-0020</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0020/">Mount service principal</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0020" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0021" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0021/">C-0021</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0021/">C-0021</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0021" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0026" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0026/">C-0026</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0026/">C-0026</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0026" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0030" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0030/">C-0030</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0030/">C-0030</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0030" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0031" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0031/">C-0031</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0031/">Delete Kubernetes events</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0031" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0034" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0034/">C-0034</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0034/">C-0034</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0034" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0035" data-sev="medium" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0035/">C-0035</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0035/">Administrative Roles</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0035" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0036" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0036/">C-0036</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0036/">C-0036</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0036" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0037" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0037/">C-0037</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0037/">C-0037</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0037" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0038" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0038/">C-0038</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0038/">C-0038</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0038" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0039" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0039/">C-0039</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0039/">C-0039</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0039" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0041" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0041/">C-0041</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0041/">C-0041</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0041" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0042" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0042/">C-0042</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0042/">C-0042</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0042" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0044" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0044/">C-0044</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0044/">C-0044</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0044" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0045" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0045/">C-0045</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0045/">C-0045</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0045" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0046" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0046/">C-0046</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0046/">C-0046</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0046" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0048" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0048/">C-0048</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0048/">C-0048</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0048" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0049" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0049/">C-0049</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0049/">C-0049</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0049" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0050" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0050/">C-0050</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0050/">Resources CPU limit and request</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0050" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0052" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0052/">C-0052</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0052/">Instance Metadata API</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0052" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0053" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0053/">C-0053</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0053/">C-0053</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0053" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0054" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0054/">C-0054</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0054/">C-0054</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0054" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0055" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0055/">C-0055</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0055/">C-0055</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0055" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0056" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0056/">C-0056</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0056/">C-0056</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0056" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0057" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0057/">C-0057</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0057/">C-0057</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0057" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0058" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0058/">C-0058</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0058/">C-0058</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0058" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0059" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0059/">C-0059</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0059/">C-0059</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0059" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0061" data-sev="low" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0061/">C-0061</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0061/">Pods in default namespace</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0061" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0062" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0062/">C-0062</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0062/">C-0062</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0062" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0063" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0063/">C-0063</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0063/">Portforwarding privileges</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0063" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0065" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0065/">C-0065</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0065/">C-0065</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0065" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0066" data-sev="medium" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0066/">C-0066</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0066/">Secret/etcd encryption enabled</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0066" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0067" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0067/">C-0067</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0067/">Audit logs enabled</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0067" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0068" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0068/">C-0068</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0068/">PSP enabled</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0068" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0069" data-sev="critical" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0069/">C-0069</a>
      <span class="ks-badge ks-badge-critical">Critical</span>
    </div>
    <a class="ks-card-title" href="c-0069/">C-0069</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0069" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0070" data-sev="critical" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0070/">C-0070</a>
      <span class="ks-badge ks-badge-critical">Critical</span>
    </div>
    <a class="ks-card-title" href="c-0070/">Enforce Kubelet client TLS authentication</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0070" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0073" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0073/">C-0073</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0073/">C-0073</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0073" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0074" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0074/">C-0074</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0074/">C-0074</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0074" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0075" data-sev="low" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0075/">C-0075</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0075/">Image pull policy on latest tag</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0075" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0076" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0076/">C-0076</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0076/">C-0076</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0076" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0077" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0077/">C-0077</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0077/">K8s common labels usage</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0077" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0078" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0078/">C-0078</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0078/">C-0078</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0078" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0079" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0079/">C-0079</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0079/">CVE-2022-0185-linux-kernel-container-escape</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0079" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0081" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0081/">C-0081</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0081/">C-0081</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0081" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0083" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0083/">C-0083</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0083/">C-0083</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0083" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0084" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0084/">C-0084</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0084/">C-0084</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0084" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0085" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0085/">C-0085</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0085/">C-0085</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0085" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0087" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0087/">C-0087</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0087/">C-0087</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0087" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0088" data-sev="high" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0088/">C-0088</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0088/">RBAC enabled</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0088" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0089" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0089/">C-0089</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0089/">C-0089</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0089" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0090" data-sev="critical" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0090/">C-0090</a>
      <span class="ks-badge ks-badge-critical">Critical</span>
    </div>
    <a class="ks-card-title" href="c-0090/">C-0090</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0090" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0091" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0091/">C-0091</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0091/">C-0091</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0091" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0092" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0092/">C-0092</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0092/">Ensure that the API server pod specification file permissions are set to 600 or more restrictive</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0092" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0093" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0093/">C-0093</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0093/">C-0093</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0093" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0094" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0094/">C-0094</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0094/">C-0094</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0094" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0095" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0095/">C-0095</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0095/">C-0095</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0095" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0096" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0096/">C-0096</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0096/">Ensure that the scheduler pod specification file permissions are set to 600 or more restrictive</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0096" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0097" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0097/">C-0097</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0097/">C-0097</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0097" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0098" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0098/">C-0098</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0098/">C-0098</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0098" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0099" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0099/">C-0099</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0099/">C-0099</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0099" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0100" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0100/">C-0100</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0100/">C-0100</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0100" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0101" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0101/">C-0101</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0101/">C-0101</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0101" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0102" data-sev="high" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0102/">C-0102</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0102/">Ensure that the etcd data directory permissions are set to 700 or more restrictive</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0102" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0103" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0103/">C-0103</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0103/">C-0103</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0103" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0104" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0104/">C-0104</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0104/">C-0104</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0104" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0105" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0105/">C-0105</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0105/">C-0105</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0105" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0106" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0106/">C-0106</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0106/">C-0106</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0106" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0107" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0107/">C-0107</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0107/">C-0107</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0107" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0108" data-sev="medium" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0108/">C-0108</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0108/">Ensure that the controller-manager.conf file permissions are set to 600 or more restrictive</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0108" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0109" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0109/">C-0109</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0109/">C-0109</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0109" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0110" data-sev="high" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0110/">C-0110</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0110/">Ensure that the Kubernetes PKI directory and file ownership is set to root:root</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0110" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0111" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0111/">C-0111</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0111/">C-0111</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0111" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0112" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0112/">C-0112</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0112/">C-0112</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0112" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0113" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0113/">C-0113</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0113/">C-0113</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0113" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0114" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0114/">C-0114</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0114/">C-0114</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0114" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0115" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0115/">C-0115</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0115/">C-0115</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0115" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0116" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0116/">C-0116</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0116/">C-0116</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0116" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0117" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0117/">C-0117</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0117/">C-0117</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0117" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0118" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0118/">C-0118</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0118/">C-0118</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0118" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0119" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0119/">C-0119</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0119/">C-0119</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0119" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0120" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0120/">C-0120</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0120/">C-0120</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0120" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0121" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0121/">C-0121</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0121/">C-0121</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0121" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0122" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0122/">C-0122</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0122/">C-0122</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0122" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0123" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0123/">C-0123</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0123/">C-0123</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0123" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0124" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0124/">C-0124</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0124/">C-0124</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0124" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0125" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0125/">C-0125</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0125/">C-0125</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0125" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0126" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0126/">C-0126</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0126/">C-0126</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0126" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0127" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0127/">C-0127</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0127/">C-0127</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0127" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0128" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0128/">C-0128</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0128/">C-0128</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0128" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0129" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0129/">C-0129</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0129/">C-0129</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0129" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0130" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0130/">C-0130</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0130/">C-0130</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0130" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0131" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0131/">C-0131</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0131/">C-0131</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0131" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0132" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0132/">C-0132</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0132/">C-0132</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0132" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0133" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0133/">C-0133</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0133/">Ensure that the API Server --audit-log-maxsize argument is set to 100 or as appropriate</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0133" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0134" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0134/">C-0134</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0134/">C-0134</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0134" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0135" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0135/">C-0135</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0135/">C-0135</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0135" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0136" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0136/">C-0136</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0136/">C-0136</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0136" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0137" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0137/">C-0137</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0137/">Ensure that the API Server --etcd-certfile and --etcd-keyfile arguments are set as appropriate</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0137" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0138" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0138/">C-0138</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0138/">C-0138</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0138" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0139" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0139/">C-0139</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0139/">C-0139</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0139" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0140" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0140/">C-0140</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0140/">C-0140</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0140" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0141" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0141/">C-0141</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0141/">Ensure that the API Server --encryption-provider-config argument is set as appropriate</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0141" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0142" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0142/">C-0142</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0142/">C-0142</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0142" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0143" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0143/">C-0143</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0143/">C-0143</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0143" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0144" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0144/">C-0144</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0144/">C-0144</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0144" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0145" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0145/">C-0145</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0145/">C-0145</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0145" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0146" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0146/">C-0146</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0146/">C-0146</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0146" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0147" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0147/">C-0147</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0147/">C-0147</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0147" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0148" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0148/">C-0148</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0148/">C-0148</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0148" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0149" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0149/">C-0149</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0149/">C-0149</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0149" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0150" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0150/">C-0150</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0150/">C-0150</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0150" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0151" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0151/">C-0151</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0151/">C-0151</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0151" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0152" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0152/">C-0152</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0152/">C-0152</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0152" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0153" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0153/">C-0153</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0153/">C-0153</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0153" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0154" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0154/">C-0154</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0154/">C-0154</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0154" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0155" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0155/">C-0155</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0155/">C-0155</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0155" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0156" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0156/">C-0156</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0156/">C-0156</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0156" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0157" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0157/">C-0157</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0157/">C-0157</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0157" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0158" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0158/">C-0158</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0158/">C-0158</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0158" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0159" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0159/">C-0159</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0159/">C-0159</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0159" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0160" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0160/">C-0160</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0160/">C-0160</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0160" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0161" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0161/">C-0161</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0161/">C-0161</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0161" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0162" data-sev="medium" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0162/">C-0162</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0162/">Ensure that the kubelet service file permissions are set to 600 or more restrictive</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0162" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0163" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0163/">C-0163</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0163/">C-0163</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0163" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0164" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0164/">C-0164</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0164/">C-0164</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0164" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0165" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0165/">C-0165</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0165/">If proxy kubeconfig file exists ensure ownership is set to root:root</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0165" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0166" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0166/">C-0166</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0166/">C-0166</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0166" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0167" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0167/">C-0167</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0167/">Ensure that the --kubeconfig kubelet.conf file ownership is set to root:root</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0167" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0168" data-sev="high" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0168/">C-0168</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0168/">Ensure that the certificate authorities file permissions are set to 600 or more restrictive</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0168" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0169" data-sev="high" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0169/">C-0169</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0169/">Ensure that the client certificate authorities file ownership is set to root:root</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0169" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0170" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0170/">C-0170</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0170/">C-0170</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0170" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0171" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0171/">C-0171</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0171/">C-0171</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0171" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0172" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0172/">C-0172</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0172/">Ensure that the --anonymous-auth argument is set to false</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0172" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0173" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0173/">C-0173</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0173/">Ensure that the --authorization-mode argument is not set to AlwaysAllow</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0173" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0174" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0174/">C-0174</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0174/">Ensure that the --client-ca-file argument is set as appropriate</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0174" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0175" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0175/">C-0175</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0175/">C-0175</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0175" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0176" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0176/">C-0176</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0176/">C-0176</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0176" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0177" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0177/">C-0177</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0177/">C-0177</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0177" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0178" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0178/">C-0178</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0178/">C-0178</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0178" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0179" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0179/">C-0179</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0179/">C-0179</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0179" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0180" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0180/">C-0180</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0180/">Ensure that the --event-qps argument is set to 0 or a level which ensures appropriate event capture</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0180" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0181" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0181/">C-0181</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0181/">C-0181</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0181" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0182" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0182/">C-0182</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0182/">C-0182</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0182" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0183" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0183/">C-0183</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0183/">C-0183</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0183" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0184" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0184/">C-0184</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0184/">C-0184</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0184" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0185" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0185/">C-0185</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0185/">C-0185</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0185" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0186" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0186/">C-0186</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0186/">C-0186</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0186" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0187" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0187/">C-0187</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0187/">C-0187</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0187" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0188" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0188/">C-0188</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0188/">C-0188</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0188" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0189" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0189/">C-0189</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0189/">C-0189</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0189" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0190" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0190/">C-0190</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0190/">C-0190</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0190" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0191" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0191/">C-0191</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0191/">C-0191</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0191" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0192" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0192/">C-0192</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0192/">C-0192</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0192" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0193" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0193/">C-0193</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0193/">C-0193</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0193" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0194" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0194/">C-0194</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0194/">C-0194</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0194" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0195" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0195/">C-0195</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0195/">C-0195</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0195" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0196" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0196/">C-0196</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0196/">C-0196</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0196" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0197" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0197/">C-0197</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0197/">C-0197</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0197" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0198" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0198/">C-0198</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0198/">C-0198</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0198" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0199" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0199/">C-0199</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0199/">C-0199</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0199" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0200" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0200/">C-0200</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0200/">C-0200</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0200" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0201" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0201/">C-0201</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0201/">C-0201</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0201" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0202" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0202/">C-0202</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0202/">C-0202</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0202" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0203" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0203/">C-0203</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0203/">C-0203</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0203" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0204" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0204/">C-0204</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0204/">C-0204</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0204" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0205" data-sev="medium" data-cat="network">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0205/">C-0205</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0205/">Ensure that the CNI in use supports Network Policies</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0205" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0206" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0206/">C-0206</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0206/">C-0206</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0206" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0207" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0207/">C-0207</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0207/">C-0207</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0207" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0208" data-sev="medium" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0208/">C-0208</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0208/">Consider external secret storage</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0208" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0209" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0209/">C-0209</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0209/">C-0209</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0209" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0210" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0210/">C-0210</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0210/">C-0210</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0210" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0211" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0211/">C-0211</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0211/">C-0211</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0211" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0212" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0212/">C-0212</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0212/">C-0212</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0212" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0213" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0213/">C-0213</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0213/">C-0213</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0213" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0214" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0214/">C-0214</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0214/">C-0214</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0214" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0215" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0215/">C-0215</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0215/">C-0215</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0215" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0216" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0216/">C-0216</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0216/">C-0216</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0216" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0217" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0217/">C-0217</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0217/">C-0217</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0217" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0218" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0218/">C-0218</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0218/">C-0218</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0218" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0219" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0219/">C-0219</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0219/">C-0219</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0219" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0220" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0220/">C-0220</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0220/">C-0220</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0220" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0221" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0221/">C-0221</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0221/">Ensure Image Vulnerability Scanning using Amazon ECR image scanning or a third party provider</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0221" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0222" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0222/">C-0222</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0222/">Minimize user access to Amazon ECR</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0222" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0223" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0223/">C-0223</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0223/">Minimize cluster access to read-only for Amazon ECR</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0223" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0225" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0225/">C-0225</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0225/">C-0225</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0225" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0226" data-sev="low" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0226/">C-0226</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0226/">Prefer using a container-optimized OS when possible</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0226" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0227" data-sev="high" data-cat="network">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0227/">C-0227</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0227/">Restrict Access to the Control Plane Endpoint</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0227" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0228" data-sev="high" data-cat="network">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0228/">C-0228</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0228/">Ensure clusters are created with Private Endpoint Enabled and Public Access Disabled</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0228" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0229" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0229/">C-0229</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0229/">Ensure clusters are created with Private Nodes</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0229" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0230" data-sev="medium" data-cat="network">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0230/">C-0230</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0230/">Ensure Network Policy is Enabled and set as appropriate</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0230" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0231" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0231/">C-0231</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0231/">Encrypt traffic to HTTPS load balancers with TLS certificates</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0231" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0232" data-sev="high" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0232/">C-0232</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0232/">Manage Kubernetes RBAC users with AWS IAM Authenticator for Kubernetes or Upgrade to AWS CLI v1.16.156</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0232" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0233" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0233/">C-0233</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0233/">C-0233</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0233" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0234" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0234/">C-0234</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0234/">C-0234</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0234" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0235" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0235/">C-0235</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0235/">C-0235</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0235" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0236" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0236/">C-0236</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0236/">C-0236</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0236" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0237" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0237/">C-0237</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0237/">C-0237</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0237" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0238" data-sev="medium" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0238/">C-0238</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0238/">Ensure that the kubeconfig file permissions are set to 644 or more restrictive</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0238" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0239" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0239/">C-0239</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0239/">C-0239</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0239" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0240" data-sev="medium" data-cat="network">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0240/">C-0240</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0240/">Ensure Network Policy is Enabled and set as appropriate</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0240" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0241" data-sev="high" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0241/">C-0241</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0241/">Use Azure RBAC for Kubernetes Authorization.</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0241" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0242" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0242/">C-0242</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0242/">C-0242</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0242" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0243" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0243/">C-0243</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0243/">Ensure Image Vulnerability Scanning using Azure Defender image scanning or a third party provider</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0243" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0244" data-sev="medium" data-cat="rbac">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0244/">C-0244</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0244/">Ensure Kubernetes Secrets are encrypted</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0244" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0245" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0245/">C-0245</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0245/">Encrypt traffic to HTTPS load balancers with TLS certificates</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0245" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0246" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0246/">C-0246</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0246/">C-0246</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0246" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0247" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0247/">C-0247</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0247/">C-0247</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0247" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0248" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0248/">C-0248</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0248/">Ensure clusters are created with Private Nodes</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0248" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0249" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0249/">C-0249</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0249/">Restrict untrusted workloads</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0249" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0250" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0250/">C-0250</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0250/">Minimize cluster access to read-only for Azure Container Registry (ACR)</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0250" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0251" data-sev="medium" data-cat="container">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0251/">C-0251</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0251/">Minimize user access to Azure Container Registry (ACR)</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0251" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0252" data-sev="high" data-cat="network">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0252/">C-0252</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0252/">Ensure clusters are created with Private Endpoint Enabled and Public Access Disabled</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0252" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0253" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0253/">C-0253</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0253/">C-0253</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0253" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0254" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0254/">C-0254</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0254/">Enable audit Logs</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0254" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0255" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0255/">C-0255</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0255/">C-0255</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0255" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0256" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0256/">C-0256</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0256/">C-0256</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0256" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0257" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0257/">C-0257</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0257/">C-0257</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0257" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0258" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0258/">C-0258</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0258/">C-0258</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0258" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0259" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0259/">C-0259</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0259/">C-0259</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0259" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0260" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0260/">C-0260</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0260/">C-0260</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0260" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0261" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0261/">C-0261</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0261/">C-0261</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0261" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0262" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0262/">C-0262</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0262/">C-0262</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0262" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0263" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0263/">C-0263</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0263/">C-0263</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0263" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0264" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0264/">C-0264</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0264/">C-0264</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0264" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0265" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0265/">C-0265</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0265/">C-0265</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0265" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0266" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0266/">C-0266</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0266/">C-0266</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0266" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0267" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0267/">C-0267</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0267/">C-0267</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0267" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0268" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0268/">C-0268</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0268/">C-0268</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0268" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0269" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0269/">C-0269</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0269/">C-0269</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0269" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0270" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0270/">C-0270</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0270/">C-0270</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0270" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0271" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0271/">C-0271</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0271/">C-0271</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0271" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0272" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0272/">C-0272</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0272/">C-0272</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0272" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0273" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0273/">C-0273</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0273/">C-0273</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0273" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0274" data-sev="high" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0274/">C-0274</a>
      <span class="ks-badge ks-badge-high">High</span>
    </div>
    <a class="ks-card-title" href="c-0274/">Verify Authenticated Service</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0274" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0275" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0275/">C-0275</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0275/">C-0275</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0275" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0276" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0276/">C-0276</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0276/">C-0276</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0276" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0277" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0277/">C-0277</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0277/">C-0277</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0277" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0278" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0278/">C-0278</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0278/">C-0278</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0278" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0279" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0279/">C-0279</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0279/">C-0279</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0279" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0280" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0280/">C-0280</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0280/">C-0280</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0280" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0281" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0281/">C-0281</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0281/">C-0281</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0281" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0282" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0282/">C-0282</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0282/">C-0282</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0282" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0283" data-sev="medium" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0283/">C-0283</a>
      <span class="ks-badge ks-badge-medium">Medium</span>
    </div>
    <a class="ks-card-title" href="c-0283/">C-0283</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0283" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
  <div class="ks-control-card" data-id="C-0284" data-sev="low" data-cat="cluster">
    <div class="ks-card-header">
      <a class="ks-card-id" href="c-0284/">C-0284</a>
      <span class="ks-badge ks-badge-low">Low</span>
    </div>
    <a class="ks-card-title" href="c-0284/">C-0284</a>
    <div class="ks-card-footer">
      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0284" title="Copy scan command">📋 Copy scan command</button>
    </div>
  </div>
</div>

<div id="ks-no-results" class="ks-no-results" style="display:none;">
  <p>No controls found matching your criteria.</p>
  <button type="button" id="ks-reset-filters" class="ks-reset-btn">Reset filters</button>
</div>
