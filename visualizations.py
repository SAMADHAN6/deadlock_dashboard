"""
Interactive Visualizations for Deadlock & Banker's Algorithm Dashboard
Provides animated replay simulation of deadlock conditions and recovery.
"""
import streamlit as st
import streamlit.components.v1 as components

def render_deadlock_replay_animation():
    """
    Renders an interactive, animated visual simulation of deadlock with Replay Mode.
    Simulates the 4 Coffman conditions step-by-step:
      1. Initial Resource Hold (Mutual Exclusion)
      2. Competing Requests (Hold & Wait)
      3. Circular Wait (Deadlock cycle confirmed)
      4. Recovery (Cycle broken via termination / preemption)
    """
    html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  :root {
    --bg: #0f172a;
    --card-bg: rgba(30, 41, 59, 0.7);
    --border: rgba(148, 163, 184, 0.2);
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --primary: #38bdf8;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --purple: #a855f7;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body {
    background: transparent;
    color: var(--text);
    padding: 2px 4px;
    overflow-x: hidden;
  }
  .container {
    background: linear-gradient(145deg, #0b1120 0%, #172033 100%);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.4);
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 10px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
  }
  .title-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .badge-live {
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.4);
    font-size: 11px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .live-dot {
    width: 6px;
    height: 6px;
    background: #ef4444;
    border-radius: 50%;
    animation: pulse-dot 1.4s infinite;
  }
  @keyframes pulse-dot {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
    100% { opacity: 1; transform: scale(1); }
  }
  .controls-bar {
    display: flex;
    align-items: center;
    gap: 5px;
    flex-wrap: wrap;
  }
  .btn {
    background: #1e293b;
    color: #f8fafc;
    border: 1px solid rgba(148, 163, 184, 0.3);
    padding: 5px 10px;
    border-radius: 7px;
    cursor: pointer;
    font-size: 11px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    transition: all 0.2s ease;
  }
  .btn:hover {
    background: #334155;
    border-color: #94a3b8;
    transform: translateY(-1px);
  }
  .btn-replay {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    border-color: #a855f7;
    color: #fff;
    box-shadow: 0 0 10px rgba(124, 58, 237, 0.4);
  }
  .btn-replay:hover {
    background: linear-gradient(135deg, #6d28d9, #4338ca);
  }
  .btn-recover {
    background: rgba(16, 185, 129, 0.15);
    border-color: #10b981;
    color: #34d399;
  }
  .btn-recover:hover {
    background: rgba(16, 185, 129, 0.3);
  }
  .mode-toggle {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    color: var(--text-muted);
    background: rgba(15, 23, 42, 0.6);
    padding: 3px 7px;
    border-radius: 6px;
    border: 1px solid var(--border);
    cursor: pointer;
    user-select: none;
  }
  .mode-toggle input {
    cursor: pointer;
  }
  .speed-select {
    background: #1e293b;
    color: #f8fafc;
    border: 1px solid rgba(148, 163, 184, 0.3);
    padding: 4px 6px;
    border-radius: 6px;
    font-size: 11px;
    cursor: pointer;
  }

  /* Stepper */
  .stepper {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
    margin-bottom: 10px;
  }
  .step-tab {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 5px 6px;
    cursor: pointer;
    text-align: center;
    transition: all 0.2s ease;
  }
  .step-tab:hover {
    background: rgba(30, 41, 59, 0.7);
  }
  .step-tab.active {
    background: rgba(56, 189, 248, 0.15);
    border-color: var(--primary);
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
  }
  .step-tab.active.danger-step {
    background: rgba(239, 68, 68, 0.15);
    border-color: var(--danger);
    box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
  }
  .step-tab.active.success-step {
    background: rgba(16, 185, 129, 0.15);
    border-color: var(--success);
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
  }
  .step-num {
    font-size: 9px;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
  }
  .step-name {
    font-size: 11px;
    font-weight: 600;
    color: var(--text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* SVG Canvas */
  .canvas-wrapper {
    position: relative;
    width: 100%;
    background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 10px;
  }
  svg {
    display: block;
    width: 100%;
    height: auto;
  }
  
  /* SVG Styles */
  .node-res {
    fill: #1e293b;
    stroke: #38bdf8;
    stroke-width: 2;
    transition: all 0.3s;
  }
  .node-proc {
    fill: #1e293b;
    stroke: #818cf8;
    stroke-width: 2;
    transition: all 0.3s;
  }
  .node-proc-deadlocked {
    fill: #450a0a !important;
    stroke: #ef4444 !important;
    animation: pulse-node 1.2s infinite;
  }
  .node-proc-recovered {
    fill: #064e3b !important;
    stroke: #10b981 !important;
  }
  .node-proc-terminated {
    fill: #1f2937 !important;
    stroke: #6b7280 !important;
    opacity: 0.5;
  }
  @keyframes pulse-node {
    0% { stroke-width: 2; filter: drop-shadow(0 0 2px rgba(239, 68, 68, 0.4)); }
    50% { stroke-width: 4; filter: drop-shadow(0 0 12px rgba(239, 68, 68, 0.9)); }
    100% { stroke-width: 2; filter: drop-shadow(0 0 2px rgba(239, 68, 68, 0.4)); }
  }

  /* Flow arrows */
  .arrow-alloc {
    stroke: #10b981;
    stroke-width: 2.5;
    fill: none;
    stroke-linecap: round;
  }
  .arrow-req {
    stroke: #f59e0b;
    stroke-width: 2.5;
    stroke-dasharray: 6, 4;
    fill: none;
    stroke-linecap: round;
    animation: flow-dash 1s linear infinite;
  }
  .arrow-req-deadlock {
    stroke: #ef4444 !important;
    stroke-width: 3.5 !important;
    animation: flow-dash 0.6s linear infinite;
  }
  @keyframes flow-dash {
    to { stroke-dashoffset: -20; }
  }

  /* Deadlock warning ring */
  .deadlock-ring {
    fill: none;
    stroke: #ef4444;
    stroke-width: 3;
    stroke-dasharray: 8, 5;
    animation: rotate-ring 6s linear infinite;
    transform-origin: 270px 145px;
    filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.8));
  }
  @keyframes rotate-ring {
    to { transform: rotate(360deg); }
  }

  /* Status message area */
  .status-box {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 12px;
  }
  .status-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
  }
  .status-title {
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .status-desc {
    font-size: 11px;
    line-height: 1.4;
    color: #cbd5e1;
    margin-bottom: 8px;
  }
  .conditions-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 5px;
    border-top: 1px solid rgba(148, 163, 184, 0.15);
    padding-top: 6px;
  }
  .condition-item {
    font-size: 10px;
    display: flex;
    align-items: center;
    gap: 5px;
    color: var(--text-muted);
  }
  .condition-item.active {
    color: #f87171;
    font-weight: 600;
  }
  .condition-item.checked {
    color: #38bdf8;
  }
  .condition-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #475569;
    flex-shrink: 0;
  }
  .condition-item.active .condition-dot {
    background: #ef4444;
    box-shadow: 0 0 6px #ef4444;
  }
  .condition-item.checked .condition-dot {
    background: #38bdf8;
  }
</style>
</head>
<body>

<div class="container">
  <!-- Header & Playback Controls -->
  <div class="header">
    <div class="title-group">
      <span style="font-size: 14px; font-weight: 700;">🔁 Deadlock Replay Simulation</span>
      <div class="badge-live" id="simBadge">
        <div class="live-dot" id="liveDot"></div>
        <span id="simStateLabel">Replaying</span>
      </div>
    </div>
    <div class="controls-bar">
      <button class="btn btn-replay" id="btnReplay" onclick="restartReplay()" title="Restart and play simulation from Step 1">
        <span>🔄</span> Replay
      </button>
      <button class="btn" id="btnPlayPause" onclick="togglePlayPause()">
        <span id="playIcon">⏸</span> <span id="playText">Pause</span>
      </button>
      <button class="btn" onclick="prevStep()" title="Previous step">⏮</button>
      <button class="btn" onclick="nextStep()" title="Next step">⏭</button>
      <button class="btn btn-recover" onclick="triggerRecovery()" title="Immediately test recovery by terminating P1">
        <span>⚡</span> Break Cycle
      </button>
      <label class="mode-toggle" title="Automatically loops replay continuously">
        <input type="checkbox" id="loopToggle" checked onchange="toggleLoop()">
        <span>Replay Loop</span>
      </label>
      <select class="speed-select" id="speedSelect" onchange="changeSpeed()" title="Animation playback speed">
        <option value="4200">0.75x</option>
        <option value="2600" selected>1x</option>
        <option value="1600">1.5x</option>
      </select>
    </div>
  </div>

  <!-- Stepper Tabs -->
  <div class="stepper">
    <div class="step-tab active" id="tab1" onclick="jumpToStep(1)">
      <div class="step-num">Step 1</div>
      <div class="step-name">1. Resource Hold</div>
    </div>
    <div class="step-tab" id="tab2" onclick="jumpToStep(2)">
      <div class="step-num">Step 2</div>
      <div class="step-name">2. Both Request</div>
    </div>
    <div class="step-tab" id="tab3" onclick="jumpToStep(3)">
      <div class="step-num">Step 3</div>
      <div class="step-name">3. Circular Deadlock</div>
    </div>
    <div class="step-tab" id="tab4" onclick="jumpToStep(4)">
      <div class="step-num">Step 4</div>
      <div class="step-name">4. Break Cycle</div>
    </div>
  </div>

  <!-- SVG Visual Canvas -->
  <div class="canvas-wrapper">
    <svg viewBox="0 0 540 280">
      <defs>
        <!-- Arrowhead markers -->
        <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981" />
        </marker>
        <marker id="arrow-cyan" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
        </marker>
        <marker id="arrow-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b" />
        </marker>
        <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444" />
        </marker>
        
        <!-- Drop shadow filter -->
        <filter id="glow-danger" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur stdDeviation="6" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>

      <!-- Center Deadlock Ring (Visible only in Step 3) -->
      <g id="deadlockRingGroup" style="display: none;">
        <circle cx="270" cy="140" r="66" class="deadlock-ring" />
        <rect x="180" y="120" width="180" height="38" rx="8" fill="#450a0a" stroke="#ef4444" stroke-width="2" filter="url(#glow-danger)" />
        <text x="270" y="144" fill="#fecaca" font-size="12" font-weight="800" text-anchor="middle">
          🚨 CIRCULAR WAIT (LOCKED)
        </text>
      </g>

      <!-- Center Recovery Glow (Visible in Step 4) -->
      <g id="recoveryGroup" style="display: none;">
        <rect x="175" y="120" width="190" height="38" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="2" />
        <text x="270" y="144" fill="#a7f3d0" font-size="12" font-weight="700" text-anchor="middle">
          ⚡ CYCLE BROKEN (RESOLVED)
        </text>
      </g>

      <!-- Resource R0: Printer -->
      <g id="nodeR0" transform="translate(60, 16)">
        <rect class="node-res" width="140" height="50" rx="10" />
        <text x="70" y="24" fill="#38bdf8" font-size="12" font-weight="700" text-anchor="middle">🖨️ Printer (R0)</text>
        <rect x="35" y="31" width="70" height="14" rx="4" fill="#0f172a" />
        <text id="r0StatusText" x="70" y="42" fill="#94a3b8" font-size="10" font-weight="600" text-anchor="middle">Held by P0</text>
      </g>

      <!-- Resource R1: Scanner -->
      <g id="nodeR1" transform="translate(340, 16)">
        <rect class="node-res" width="140" height="50" rx="10" />
        <text x="70" y="24" fill="#38bdf8" font-size="12" font-weight="700" text-anchor="middle">📄 Scanner (R1)</text>
        <rect x="35" y="31" width="70" height="14" rx="4" fill="#0f172a" />
        <text id="r1StatusText" x="70" y="42" fill="#94a3b8" font-size="10" font-weight="600" text-anchor="middle">Held by P1</text>
      </g>

      <!-- Process P0 -->
      <g id="nodeP0" transform="translate(60, 210)">
        <rect id="rectP0" class="node-proc" width="140" height="52" rx="10" />
        <text id="p0Title" x="70" y="25" fill="#f8fafc" font-size="12" font-weight="700" text-anchor="middle">⚙️ Process P0</text>
        <rect id="badgeBgP0" x="25" y="32" width="90" height="15" rx="4" fill="#0f172a" />
        <text id="p0Badge" x="70" y="43" fill="#38bdf8" font-size="10" font-weight="600" text-anchor="middle">Holds Printer</text>
      </g>

      <!-- Process P1 -->
      <g id="nodeP1" transform="translate(340, 210)">
        <rect id="rectP1" class="node-proc" width="140" height="52" rx="10" />
        <text id="p1Title" x="70" y="25" fill="#f8fafc" font-size="12" font-weight="700" text-anchor="middle">⚙️ Process P1</text>
        <rect id="badgeBgP1" x="25" y="32" width="90" height="15" rx="4" fill="#0f172a" />
        <text id="p1Badge" x="70" y="43" fill="#a855f7" font-size="10" font-weight="600" text-anchor="middle">Holds Scanner</text>
      </g>

      <!-- Allocation Arrow 1: Printer (R0) -> P0 -->
      <g id="edgeAllocR0P0">
        <path d="M 130 66 L 130 202" class="arrow-alloc" marker-end="url(#arrow-green)" />
        <rect x="88" y="125" width="84" height="18" rx="4" fill="#064e3b" stroke="#059669" stroke-width="1" />
        <text x="130" y="138" fill="#a7f3d0" font-size="9" font-weight="700" text-anchor="middle">ALLOCATED</text>
      </g>

      <!-- Allocation Arrow 2: Scanner (R1) -> P1 -->
      <g id="edgeAllocR1P1">
        <path d="M 410 66 L 410 202" class="arrow-alloc" marker-end="url(#arrow-green)" />
        <rect x="368" y="125" width="84" height="18" rx="4" fill="#064e3b" stroke="#059669" stroke-width="1" />
        <text x="410" y="138" fill="#a7f3d0" font-size="9" font-weight="700" text-anchor="middle">ALLOCATED</text>
      </g>

      <!-- Request Arrow 1: P0 -> Scanner (R1) (Active in Step 2, 3) -->
      <g id="edgeReqP0R1" style="display: none;">
        <path id="pathReqP0R1" d="M 195 212 L 345 74" class="arrow-req" marker-end="url(#arrow-amber)" />
        <rect x="238" y="98" width="84" height="18" rx="4" fill="#451a03" stroke="#d97706" stroke-width="1" id="reqBoxP0R1" />
        <text x="280" y="111" fill="#fde68a" font-size="9" font-weight="700" text-anchor="middle" id="reqTextP0R1">WAITS FOR R1</text>
      </g>

      <!-- Request Arrow 2: P1 -> Printer (R0) (Active in Step 2, 3) -->
      <g id="edgeReqP1R0" style="display: none;">
        <path id="pathReqP1R0" d="M 345 212 L 195 74" class="arrow-req" marker-end="url(#arrow-amber)" />
        <rect x="218" y="160" width="84" height="18" rx="4" fill="#451a03" stroke="#d97706" stroke-width="1" id="reqBoxP1R0" />
        <text x="260" y="173" fill="#fde68a" font-size="9" font-weight="700" text-anchor="middle" id="reqTextP1R0">WAITS FOR R0</text>
      </g>

      <!-- Recovery Edge: Scanner (R1) -> P0 (Active in Step 4) -->
      <g id="edgeRecoveryR1P0" style="display: none;">
        <path d="M 355 68 L 185 210" class="arrow-alloc" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arrow-cyan)" />
        <rect x="220" y="132" width="120" height="20" rx="5" fill="#0369a1" stroke="#38bdf8" stroke-width="1" />
        <text x="280" y="146" fill="#e0f2fe" font-size="9" font-weight="700" text-anchor="middle">GRANTED TO P0</text>
      </g>
    </svg>
  </div>

  <!-- Status & Explain Panel -->
  <div class="status-box">
    <div class="status-header">
      <div class="status-title" id="statusTitle">
        <span>🔹 Step 1 of 4: Initial Resource Allocation</span>
      </div>
      <div id="statusBadge" style="font-size: 10px; padding: 2px 7px; border-radius: 6px; background: rgba(56, 189, 248, 0.2); color: #38bdf8; font-weight: 700;">
        NORMAL STATE
      </div>
    </div>
    <div class="status-desc" id="statusDesc">
      P0 holds Printer (R0) and P1 holds Scanner (R1). Both resources have 1 instance and mutual exclusion is active.
    </div>
    <div class="conditions-grid">
      <div class="condition-item checked" id="condME">
        <div class="condition-dot"></div>
        <span>1. Mutual Exclusion: Active (1 instance)</span>
      </div>
      <div class="condition-item" id="condHW">
        <div class="condition-dot"></div>
        <span>2. Hold & Wait: Inactive</span>
      </div>
      <div class="condition-item checked" id="condNP">
        <div class="condition-dot"></div>
        <span>3. No Preemption: Active (No seizing)</span>
      </div>
      <div class="condition-item" id="condCW">
        <div class="condition-dot"></div>
        <span>4. Circular Wait: None</span>
      </div>
    </div>
  </div>
</div>

<script>
  let currentStep = 1;
  let isPlaying = true;
  let isLooping = true;
  let timer = null;
  let stepDuration = 2600;

  const stepsData = {
    1: {
      badgeText: "STABLE",
      badgeClass: "background: rgba(16, 185, 129, 0.2); color: #34d399;",
      title: "🔹 Step 1: Initial Allocation (Resources Held)",
      desc: "Each process has safely acquired one resource. <b>P0 holds Printer (R0)</b> and <b>P1 holds Scanner (R1)</b>. Neither is requesting anything yet.",
      condHW: false,
      condCW: false,
      isDeadlock: false,
      isRecovery: false
    },
    2: {
      badgeText: "HOLD & WAIT",
      badgeClass: "background: rgba(245, 158, 11, 0.2); color: #fbbf24;",
      title: "⚠️ Step 2: Competing Requests (Hold & Wait Begins)",
      desc: "P0 keeps holding Printer and now <b>requests Scanner</b> (held by P1). Meanwhile, P1 keeps holding Scanner and <b>requests Printer</b> (held by P0). Both processes enter waiting states.",
      condHW: true,
      condCW: false,
      isDeadlock: false,
      isRecovery: false
    },
    3: {
      badgeText: "DEADLOCKED 🚨",
      badgeClass: "background: rgba(239, 68, 68, 0.25); color: #f87171;",
      title: "🚨 Step 3: Circular Wait Cycle Formed (DEADLOCK)",
      desc: "<b>All 4 Coffman conditions are fulfilled!</b> P0 waits for P1 to release Scanner, and P1 waits for P0 to release Printer. Because no preemption is allowed, both wait forever.",
      condHW: true,
      condCW: true,
      isDeadlock: true,
      isRecovery: false
    },
    4: {
      badgeText: "RECOVERED ✅",
      badgeClass: "background: rgba(16, 185, 129, 0.2); color: #34d399;",
      title: "⚡ Step 4: Recovery (Cycle Broken)",
      desc: "The OS initiates recovery: <b>P1 is terminated</b>, releasing Scanner (R1). Scanner is immediately granted to P0. P0 successfully finishes its task and releases both resources!",
      condHW: false,
      condCW: false,
      isDeadlock: false,
      isRecovery: true
    }
  };

  function updateUI() {
    // Update step tabs
    for (let s = 1; s <= 4; s++) {
      const tab = document.getElementById(`tab${s}`);
      tab.classList.remove("active", "danger-step", "success-step");
      if (s === currentStep) {
        tab.classList.add("active");
        if (s === 3) tab.classList.add("danger-step");
        if (s === 4) tab.classList.add("success-step");
      }
    }

    const data = stepsData[currentStep];

    // Status box
    document.getElementById("statusTitle").innerHTML = `<span>${data.title}</span>`;
    document.getElementById("statusDesc").innerHTML = data.desc;
    const badge = document.getElementById("statusBadge");
    badge.innerText = data.badgeText;
    badge.style.cssText = `font-size: 10px; padding: 2px 7px; border-radius: 6px; font-weight: 700; ${data.badgeClass}`;

    // Conditions
    const hwEl = document.getElementById("condHW");
    hwEl.className = data.condHW ? "condition-item active" : "condition-item";
    hwEl.querySelector("span").innerText = data.condHW ? "2. Hold & Wait: Active (Holding while asking)" : "2. Hold & Wait: Inactive";

    const cwEl = document.getElementById("condCW");
    cwEl.className = data.condCW ? "condition-item active" : "condition-item";
    cwEl.querySelector("span").innerText = data.condCW ? "4. Circular Wait: Formed (P0 ⟲ P1 Cycle!)" : "4. Circular Wait: None";

    // SVG elements
    const deadlockGroup = document.getElementById("deadlockRingGroup");
    const recoveryGroup = document.getElementById("recoveryGroup");
    const edgeAllocR0P0 = document.getElementById("edgeAllocR0P0");
    const edgeAllocR1P1 = document.getElementById("edgeAllocR1P1");
    const edgeReqP0R1 = document.getElementById("edgeReqP0R1");
    const edgeReqP1R0 = document.getElementById("edgeReqP1R0");
    const edgeRecoveryR1P0 = document.getElementById("edgeRecoveryR1P0");

    const rectP0 = document.getElementById("rectP0");
    const rectP1 = document.getElementById("rectP1");
    const p0Badge = document.getElementById("p0Badge");
    const p1Badge = document.getElementById("p1Badge");
    const r0Text = document.getElementById("r0StatusText");
    const r1Text = document.getElementById("r1StatusText");

    const simStateLabel = document.getElementById("simStateLabel");
    const liveDot = document.getElementById("liveDot");

    if (currentStep === 1) {
      deadlockGroup.style.display = "none";
      recoveryGroup.style.display = "none";
      edgeAllocR0P0.style.display = "block";
      edgeAllocR1P1.style.display = "block";
      edgeReqP0R1.style.display = "none";
      edgeReqP1R0.style.display = "none";
      edgeRecoveryR1P0.style.display = "none";

      rectP0.className.baseVal = "node-proc";
      rectP1.className.baseVal = "node-proc";
      p0Badge.textContent = "Holds Printer";
      p0Badge.setAttribute("fill", "#38bdf8");
      p1Badge.textContent = "Holds Scanner";
      p1Badge.setAttribute("fill", "#a855f7");
      r0Text.textContent = "Held by P0";
      r1Text.textContent = "Held by P1";

      simStateLabel.textContent = isPlaying ? "Replay: Step 1" : "Paused: Step 1";
      liveDot.style.background = "#10b981";
    }
    else if (currentStep === 2) {
      deadlockGroup.style.display = "none";
      recoveryGroup.style.display = "none";
      edgeAllocR0P0.style.display = "block";
      edgeAllocR1P1.style.display = "block";
      edgeReqP0R1.style.display = "block";
      edgeReqP1R0.style.display = "block";
      edgeRecoveryR1P0.style.display = "none";

      document.getElementById("pathReqP0R1").className.baseVal = "arrow-req";
      document.getElementById("pathReqP0R1").setAttribute("marker-end", "url(#arrow-amber)");
      document.getElementById("reqBoxP0R1").setAttribute("fill", "#451a03");
      document.getElementById("reqBoxP0R1").setAttribute("stroke", "#d97706");
      document.getElementById("reqTextP0R1").setAttribute("fill", "#fde68a");

      document.getElementById("pathReqP1R0").className.baseVal = "arrow-req";
      document.getElementById("pathReqP1R0").setAttribute("marker-end", "url(#arrow-amber)");
      document.getElementById("reqBoxP1R0").setAttribute("fill", "#451a03");
      document.getElementById("reqBoxP1R0").setAttribute("stroke", "#d97706");
      document.getElementById("reqTextP1R0").setAttribute("fill", "#fde68a");

      rectP0.className.baseVal = "node-proc";
      rectP1.className.baseVal = "node-proc";
      p0Badge.textContent = "Waiting for R1";
      p0Badge.setAttribute("fill", "#fbbf24");
      p1Badge.textContent = "Waiting for R0";
      p1Badge.setAttribute("fill", "#fbbf24");
      r0Text.textContent = "Locked (P0)";
      r1Text.textContent = "Locked (P1)";

      simStateLabel.textContent = isPlaying ? "Replay: Step 2" : "Paused: Step 2";
      liveDot.style.background = "#f59e0b";
    }
    else if (currentStep === 3) {
      deadlockGroup.style.display = "block";
      recoveryGroup.style.display = "none";
      edgeAllocR0P0.style.display = "block";
      edgeAllocR1P1.style.display = "block";
      edgeReqP0R1.style.display = "block";
      edgeReqP1R0.style.display = "block";
      edgeRecoveryR1P0.style.display = "none";

      document.getElementById("pathReqP0R1").className.baseVal = "arrow-req arrow-req-deadlock";
      document.getElementById("pathReqP0R1").setAttribute("marker-end", "url(#arrow-red)");
      document.getElementById("reqBoxP0R1").setAttribute("fill", "#7f1d1d");
      document.getElementById("reqBoxP0R1").setAttribute("stroke", "#ef4444");
      document.getElementById("reqTextP0R1").setAttribute("fill", "#fecaca");

      document.getElementById("pathReqP1R0").className.baseVal = "arrow-req arrow-req-deadlock";
      document.getElementById("pathReqP1R0").setAttribute("marker-end", "url(#arrow-red)");
      document.getElementById("reqBoxP1R0").setAttribute("fill", "#7f1d1d");
      document.getElementById("reqBoxP1R0").setAttribute("stroke", "#ef4444");
      document.getElementById("reqTextP1R0").setAttribute("fill", "#fecaca");

      rectP0.className.baseVal = "node-proc node-proc-deadlocked";
      rectP1.className.baseVal = "node-proc node-proc-deadlocked";
      p0Badge.textContent = "🔒 DEADLOCKED";
      p0Badge.setAttribute("fill", "#fca5a5");
      p1Badge.textContent = "🔒 DEADLOCKED";
      p1Badge.setAttribute("fill", "#fca5a5");
      r0Text.textContent = "Contested";
      r1Text.textContent = "Contested";

      simStateLabel.textContent = "DEADLOCK!";
      liveDot.style.background = "#ef4444";
    }
    else if (currentStep === 4) {
      deadlockGroup.style.display = "none";
      recoveryGroup.style.display = "block";
      edgeAllocR0P0.style.display = "block";
      edgeAllocR1P1.style.display = "none"; // P1 released Scanner
      edgeReqP0R1.style.display = "none";
      edgeReqP1R0.style.display = "none";
      edgeRecoveryR1P0.style.display = "block"; // Scanner given to P0

      rectP0.className.baseVal = "node-proc node-proc-recovered";
      rectP1.className.baseVal = "node-proc node-proc-terminated";
      p0Badge.textContent = "✅ COMPLETED";
      p0Badge.setAttribute("fill", "#6ee7b7");
      p1Badge.textContent = "❌ TERMINATED";
      p1Badge.setAttribute("fill", "#9ca3af");
      r0Text.textContent = "Held by P0";
      r1Text.textContent = "Granted to P0";

      simStateLabel.textContent = isPlaying ? "Replay: Step 4" : "Resolved";
      liveDot.style.background = "#10b981";
    }
  }

  function startTimer() {
    clearTimeout(timer);
    if (!isPlaying) return;
    const duration = (currentStep === 3) ? stepDuration * 1.3 : stepDuration;
    timer = setTimeout(() => {
      if (currentStep < 4) {
        currentStep++;
        updateUI();
        startTimer();
      } else {
        if (isLooping) {
          currentStep = 1;
          updateUI();
          startTimer();
        } else {
          pauseSimulation();
        }
      }
    }, duration);
  }

  function togglePlayPause() {
    if (isPlaying) {
      pauseSimulation();
    } else {
      resumeSimulation();
    }
  }

  function pauseSimulation() {
    isPlaying = false;
    clearTimeout(timer);
    document.getElementById("playIcon").textContent = "▶";
    document.getElementById("playText").textContent = "Play";
    const simStateLabel = document.getElementById("simStateLabel");
    simStateLabel.textContent = "Paused";
  }

  function resumeSimulation() {
    isPlaying = true;
    document.getElementById("playIcon").textContent = "⏸";
    document.getElementById("playText").textContent = "Pause";
    updateUI();
    startTimer();
  }

  function restartReplay() {
    currentStep = 1;
    isPlaying = true;
    document.getElementById("playIcon").textContent = "⏸";
    document.getElementById("playText").textContent = "Pause";
    updateUI();
    startTimer();
  }

  function triggerRecovery() {
    currentStep = 4;
    updateUI();
    if (isPlaying) startTimer();
  }

  function jumpToStep(step) {
    currentStep = step;
    updateUI();
    if (isPlaying) startTimer();
  }

  function nextStep() {
    currentStep = (currentStep % 4) + 1;
    updateUI();
    if (isPlaying) startTimer();
  }

  function prevStep() {
    currentStep = (currentStep === 1) ? 4 : currentStep - 1;
    updateUI();
    if (isPlaying) startTimer();
  }

  function toggleLoop() {
    isLooping = document.getElementById("loopToggle").checked;
    if (isLooping && !isPlaying) {
      resumeSimulation();
    }
  }

  function changeSpeed() {
    stepDuration = parseInt(document.getElementById("speedSelect").value);
    if (isPlaying) startTimer();
  }

  // Initialize immediately
  updateUI();
  startTimer();
</script>
</body>
</html>
    """
    components.html(html_code, height=525)
