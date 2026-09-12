import os

html_code = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>INFRAcare — Building Better Cities Together</title>

  <!-- Leaflet Map CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <!-- Font Awesome 6 Pro Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />

  <!-- Google Fonts: Plus Jakarta Sans & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

  <style>
    /* ==========================================================================
       1. CORE DESIGN SYSTEM & THEME
       ========================================================================== */
    :root {
      --bg-dark: #070b14;
      --bg-card: rgba(15, 23, 42, 0.78);
      --bg-card-hover: rgba(30, 41, 59, 0.85);
      --bg-surface: rgba(11, 17, 33, 0.92);
      --primary: #3b82f6;
      --primary-glow: rgba(59, 130, 246, 0.45);
      --accent-cyan: #06b6d4;
      --accent-teal: #14b8a6;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --danger-glow: rgba(239, 68, 68, 0.5);
      --purple: #a855f7;
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      
      --glass-border: rgba(255, 255, 255, 0.12);
      --glass-border-light: rgba(255, 255, 255, 0.18);
      --glass-shadow: 0 20px 50px rgba(0, 0, 0, 0.65), 0 0 1px 1px rgba(255, 255, 255, 0.08);
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-xl: 26px;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      user-select: none;
    }

    /* ==========================================================================
       2. FULLSCREEN MAP CANVAS (HERO)
       ========================================================================== */
    #map-viewport {
      position: absolute;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 1;
      background: #090d16;
    }
    #map { width: 100%; height: 100%; }

    /* ==========================================================================
       3. TOP FLOATING NAVIGATION BAR
       ========================================================================== */
    #top-nav {
      position: absolute;
      top: 16px;
      left: 20px;
      right: 20px;
      height: 64px;
      z-index: 500;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 18px;
      background: rgba(13, 20, 36, 0.78);
      backdrop-filter: blur(20px) saturate(180%);
      -webkit-backdrop-filter: blur(20px) saturate(180%);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-lg);
      box-shadow: var(--glass-shadow);
      pointer-events: auto;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
    }
    .brand-logo-badge {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: linear-gradient(135deg, #2563eb, #06b6d4);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      color: #fff;
      box-shadow: 0 0 20px var(--primary-glow);
    }
    .brand-title-wrap h1 {
      font-size: 17px;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.1;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .brand-title-wrap h1 span { color: var(--accent-cyan); font-weight: 900; }
    .brand-title-wrap p {
      font-size: 10.5px;
      font-weight: 600;
      color: var(--text-muted);
      letter-spacing: 0.04em;
    }

    /* Nav center pills */
    .nav-pills {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(0, 0, 0, 0.35);
      padding: 5px;
      border-radius: 14px;
      border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .nav-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s ease;
      background: transparent;
      font-family: inherit;
    }
    .nav-pill:hover { color: var(--text-main); background: rgba(255, 255, 255, 0.05); }
    .nav-pill.active {
      background: var(--primary);
      color: #fff;
      box-shadow: 0 4px 14px var(--primary-glow);
      border-color: rgba(255, 255, 255, 0.2);
    }
    .nav-pill.report-btn {
      background: linear-gradient(135deg, #2563eb, #0ea5e9);
      color: #fff;
      box-shadow: 0 4px 16px rgba(14, 165, 233, 0.45);
      animation: pulseGlow 3s infinite;
    }
    @keyframes pulseGlow {
      0%, 100% { box-shadow: 0 0 16px rgba(59, 130, 246, 0.4); }
      50% { box-shadow: 0 0 24px rgba(6, 182, 212, 0.7); }
    }

    /* Right profile & actions */
    .nav-right-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .icon-action-btn {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--glass-border);
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 15px;
      cursor: pointer;
      position: relative;
      transition: all 0.2s;
    }
    .icon-action-btn:hover { color: var(--text-main); background: rgba(255, 255, 255, 0.1); border-color: var(--primary); }
    .badge-dot {
      position: absolute;
      top: -2px;
      right: -2px;
      background: var(--danger);
      color: #fff;
      font-size: 10px;
      font-weight: 800;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 2px solid #0b1121;
    }

    /* Role switcher select */
    .role-badge-select {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(0, 0, 0, 0.4);
      padding: 4px 6px 4px 10px;
      border-radius: 12px;
      border: 1px solid var(--glass-border);
    }
    .role-avatar {
      width: 28px;
      height: 28px;
      border-radius: 8px;
      background: linear-gradient(135deg, #6366f1, #3b82f6);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 800;
      color: #fff;
    }
    .role-dropdown {
      background: transparent;
      border: none;
      color: var(--text-main);
      font-size: 12.5px;
      font-weight: 700;
      font-family: inherit;
      cursor: pointer;
      outline: none;
    }
    .role-dropdown option { background: #0f172a; color: #fff; font-weight: 600; }

    /* ==========================================================================
       4. MAP FLOATING SEARCH & CONTROLS
       ========================================================================== */
    .map-search-bar {
      position: absolute;
      top: 94px;
      left: 24px;
      width: 360px;
      z-index: 400;
      background: rgba(13, 20, 36, 0.82);
      backdrop-filter: blur(16px);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      box-shadow: var(--glass-shadow);
      display: flex;
      align-items: center;
      padding: 8px 14px;
      gap: 10px;
      transition: all 0.2s;
    }
    .map-search-bar:focus-within {
      border-color: var(--primary);
      box-shadow: 0 0 20px var(--primary-glow);
    }
    .map-search-bar input {
      flex: 1;
      background: transparent;
      border: none;
      color: var(--text-main);
      font-family: inherit;
      font-size: 13px;
      font-weight: 500;
      outline: none;
    }
    .map-search-bar input::placeholder { color: var(--text-dim); }

    /* Layer Switcher Top-Right */
    .map-layer-selector {
      position: absolute;
      top: 94px;
      right: 24px;
      z-index: 400;
      display: flex;
      background: rgba(13, 20, 36, 0.85);
      backdrop-filter: blur(16px);
      padding: 4px;
      border-radius: var(--radius-md);
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-shadow);
      gap: 4px;
    }
    .layer-toggle-btn {
      padding: 7px 14px;
      border-radius: 10px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: inherit;
      transition: all 0.2s;
    }
    .layer-toggle-btn.active {
      background: var(--primary);
      color: #fff;
      box-shadow: 0 2px 10px var(--primary-glow);
    }

    /* Right Vertical Map Toolbar */
    .map-vertical-toolbar {
      position: absolute;
      top: 156px;
      right: 24px;
      z-index: 400;
      display: flex;
      flex-direction: column;
      gap: 8px;
      background: rgba(13, 20, 36, 0.85);
      backdrop-filter: blur(16px);
      padding: 8px;
      border-radius: var(--radius-md);
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-shadow);
    }
    .toolbar-tool-btn {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.06);
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 15px;
      cursor: pointer;
      transition: all 0.2s;
      position: relative;
    }
    .toolbar-tool-btn:hover, .toolbar-tool-btn.active {
      color: #fff;
      background: var(--primary);
      border-color: var(--primary);
      box-shadow: 0 0 14px var(--primary-glow);
    }
    .toolbar-tooltip {
      position: absolute;
      right: 50px;
      background: rgba(15, 23, 42, 0.95);
      color: #fff;
      padding: 5px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      white-space: nowrap;
      border: 1px solid var(--glass-border);
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .toolbar-tool-btn:hover .toolbar-tooltip { opacity: 1; transform: translateX(-4px); }

    /* Bottom Map Priority Legend */
    .map-priority-legend {
      position: absolute;
      bottom: 24px;
      left: 24px;
      z-index: 400;
      background: rgba(13, 20, 36, 0.85);
      backdrop-filter: blur(16px);
      padding: 10px 16px;
      border-radius: var(--radius-md);
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-shadow);
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 11.5px;
      font-weight: 700;
    }
    .legend-item { display: flex; align-items: center; gap: 6px; }
    .legend-beacon { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
    .beacon-critical { background: var(--danger); box-shadow: 0 0 10px var(--danger); }
    .beacon-high { background: var(--warning); box-shadow: 0 0 8px var(--warning); }
    .beacon-medium { background: var(--accent-cyan); box-shadow: 0 0 8px var(--accent-cyan); }
    .beacon-low { background: var(--success); box-shadow: 0 0 8px var(--success); }

    /* ==========================================================================
       5. FLOATING 3-STEP REPORT GLASS PANEL (HERO UX)
       ========================================================================== */
    #report-glass-panel {
      position: absolute;
      top: 94px;
      left: 24px;
      width: 480px;
      max-width: calc(100vw - 48px);
      max-height: calc(100vh - 120px);
      z-index: 600;
      background: rgba(13, 20, 38, 0.82);
      backdrop-filter: blur(24px) saturate(190%);
      -webkit-backdrop-filter: blur(24px) saturate(190%);
      border: 1px solid var(--glass-border-light);
      border-radius: var(--radius-xl);
      box-shadow: var(--glass-shadow), 0 0 40px rgba(0, 0, 0, 0.5);
      display: none;
      flex-direction: column;
      overflow: hidden;
      animation: panelSlideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }
    #report-glass-panel.open { display: flex; }

    @keyframes panelSlideIn {
      from { opacity: 0; transform: translateY(20px) scale(0.97); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .panel-header {
      padding: 20px 24px 16px;
      border-bottom: 1px solid var(--glass-border);
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      position: relative;
    }
    .panel-header-info h2 {
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -0.01em;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .panel-header-info p {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 3px;
    }
    .panel-close-btn {
      width: 32px;
      height: 32px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--glass-border);
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 14px;
      transition: all 0.2s;
    }
    .panel-close-btn:hover { background: rgba(239, 68, 68, 0.2); color: var(--danger); border-color: var(--danger); }

    /* 3-Step Progress Stepper */
    .stepper-wrap {
      padding: 14px 24px;
      background: rgba(0, 0, 0, 0.25);
      border-bottom: 1px solid var(--glass-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
    }
    .step-node {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      z-index: 2;
    }
    .step-circle {
      width: 26px;
      height: 26px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--glass-border);
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.25s;
    }
    .step-title { font-size: 12px; font-weight: 700; color: var(--text-muted); transition: color 0.25s; }
    .step-node.active .step-circle {
      background: var(--primary);
      border-color: var(--primary);
      color: #fff;
      box-shadow: 0 0 12px var(--primary-glow);
    }
    .step-node.active .step-title { color: #fff; }
    .step-node.completed .step-circle {
      background: var(--success);
      border-color: var(--success);
      color: #fff;
    }
    .step-connector {
      flex: 1;
      height: 2px;
      background: rgba(255, 255, 255, 0.1);
      margin: 0 8px;
    }

    /* Panel Content */
    .panel-body {
      padding: 22px 24px;
      overflow-y: auto;
      flex: 1;
    }

    .form-step-content { display: none; }
    .form-step-content.active { display: block; animation: stepFade 0.25s ease; }
    @keyframes stepFade { from { opacity: 0; transform: translateX(10px); } to { opacity: 1; transform: translateX(0); } }

    /* Category selection cards */
    .cat-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 16px;
    }
    .cat-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      padding: 12px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      transition: all 0.2s;
    }
    .cat-card:hover { background: rgba(255, 255, 255, 0.08); border-color: rgba(255, 255, 255, 0.2); }
    .cat-card.selected {
      background: rgba(59, 130, 246, 0.2);
      border-color: var(--primary);
      box-shadow: 0 0 16px rgba(59, 130, 246, 0.3);
    }
    .cat-icon { font-size: 20px; }
    .cat-label h4 { font-size: 13px; font-weight: 700; }
    .cat-label p { font-size: 10px; color: var(--text-muted); }

    /* Severity Radio buttons */
    .severity-row {
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
    }
    .sev-chip {
      flex: 1;
      padding: 8px 4px;
      border-radius: var(--radius-sm);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--glass-border);
      text-align: center;
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s;
    }
    .sev-chip:hover { border-color: rgba(255,255,255,0.2); }
    .sev-chip.selected[data-sev="Critical"] { background: rgba(239, 68, 68, 0.25); border-color: var(--danger); color: #fca5a5; }
    .sev-chip.selected[data-sev="High"] { background: rgba(245, 158, 11, 0.25); border-color: var(--warning); color: #fde68a; }
    .sev-chip.selected[data-sev="Medium"] { background: rgba(59, 130, 246, 0.25); border-color: var(--primary); color: #93c5fd; }
    .sev-chip.selected[data-sev="Low"] { background: rgba(16, 185, 129, 0.25); border-color: var(--success); color: #a7f3d0; }

    /* Form Fields */
    .field-group { margin-bottom: 16px; }
    .field-label {
      display: block;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      margin-bottom: 6px;
    }
    .glass-input, .glass-textarea {
      width: 100%;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-sm);
      padding: 10px 14px;
      color: var(--text-main);
      font-size: 13.5px;
      font-family: inherit;
      transition: all 0.2s;
      outline: none;
    }
    .glass-input:focus, .glass-textarea:focus {
      border-color: var(--primary);
      box-shadow: 0 0 14px var(--primary-glow);
    }
    .glass-textarea { min-height: 80px; resize: vertical; }

    /* Custom Photo Upload Component */
    .upload-zone {
      border: 2px dashed rgba(255, 255, 255, 0.16);
      border-radius: var(--radius-md);
      background: rgba(0, 0, 0, 0.25);
      padding: 20px 16px;
      text-align: center;
      cursor: pointer;
      transition: all 0.25s ease;
      position: relative;
    }
    .upload-zone:hover, .upload-zone.dragover {
      border-color: var(--primary);
      background: rgba(59, 130, 246, 0.08);
    }
    .upload-icon { font-size: 28px; color: var(--primary); margin-bottom: 8px; }
    .upload-zone h4 { font-size: 13px; font-weight: 700; margin-bottom: 3px; }
    .upload-zone p { font-size: 11px; color: var(--text-muted); }

    /* Photo Preview Card */
    .photo-preview-card {
      display: none;
      position: relative;
      background: rgba(0, 0, 0, 0.45);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      overflow: hidden;
      padding: 8px;
      gap: 12px;
      align-items: center;
      margin-top: 10px;
    }
    .photo-preview-card.show { display: flex; animation: stepFade 0.2s ease; }
    .photo-thumb {
      width: 64px;
      height: 64px;
      border-radius: 8px;
      object-fit: cover;
      border: 1px solid var(--glass-border);
    }
    .photo-meta { flex: 1; overflow: hidden; }
    .photo-name { font-size: 12.5px; font-weight: 700; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; }
    .photo-size { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
    .photo-remove-btn {
      padding: 6px 10px;
      background: rgba(239, 68, 68, 0.2);
      border: 1px solid var(--danger);
      color: #fca5a5;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s;
    }
    .photo-remove-btn:hover { background: var(--danger); color: #fff; }

    /* Step 2 Location UI */
    .loc-action-card {
      background: rgba(59, 130, 246, 0.1);
      border: 1px solid var(--primary);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 16px;
      text-align: center;
    }
    .gps-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(135deg, #2563eb, #06b6d4);
      color: #fff;
      padding: 10px 20px;
      border-radius: 12px;
      font-size: 13.5px;
      font-weight: 800;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 16px var(--primary-glow);
      transition: all 0.2s;
      font-family: inherit;
    }
    .gps-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px var(--primary-glow); }
    .gps-btn.locating { animation: radarPulse 1s infinite alternate; }

    @keyframes radarPulse {
      from { transform: scale(1); box-shadow: 0 0 10px var(--primary-glow); }
      to { transform: scale(1.05); box-shadow: 0 0 25px rgba(6, 182, 212, 0.8); }
    }

    .coords-display-box {
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      padding: 14px;
      margin-top: 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-family: 'JetBrains Mono', monospace;
    }
    .coords-row { display: flex; justify-content: space-between; font-size: 12px; }
    .coords-val { color: var(--accent-cyan); font-weight: 600; }

    /* Step 3 Review & AI Priority */
    .review-summary-card {
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .review-item { display: flex; justify-content: space-between; font-size: 12.5px; }
    .review-label { color: var(--text-muted); }
    .review-val { font-weight: 700; color: #fff; }

    .ai-priority-box {
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(168, 85, 247, 0.15));
      border: 1px solid rgba(168, 85, 247, 0.4);
      border-radius: var(--radius-md);
      padding: 14px 16px;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .ai-priority-icon { font-size: 24px; color: var(--purple); }
    .ai-priority-info h4 { font-size: 13px; font-weight: 800; color: #fff; }
    .ai-priority-info p { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

    /* Submission multi-step progress */
    .submit-progress-overlay {
      display: none;
      background: rgba(13, 20, 36, 0.95);
      border-radius: var(--radius-xl);
      position: absolute;
      inset: 0;
      z-index: 10;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px;
      text-align: center;
    }
    .submit-progress-overlay.show { display: flex; animation: stepFade 0.3s ease; }
    .spinner-ring {
      width: 54px;
      height: 54px;
      border: 4px solid rgba(59, 130, 246, 0.2);
      border-top-color: var(--primary);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin-bottom: 20px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    .progress-step-txt {
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 6px;
    }
    .progress-sub-txt { font-size: 12px; color: var(--text-muted); }

    /* Success Card */
    .success-badge-icon {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: rgba(16, 185, 129, 0.2);
      border: 2px solid var(--success);
      color: var(--success);
      font-size: 26px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 16px;
      box-shadow: 0 0 24px rgba(16, 185, 129, 0.4);
    }

    /* Panel Footer actions */
    .panel-footer {
      padding: 16px 24px;
      border-top: 1px solid var(--glass-border);
      background: rgba(0, 0, 0, 0.2);
      display: flex;
      justify-content: space-between;
      gap: 12px;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 18px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid transparent;
      font-family: inherit;
      transition: all 0.2s;
    }
    .btn-glass {
      background: rgba(255, 255, 255, 0.06);
      border-color: var(--glass-border);
      color: var(--text-main);
    }
    .btn-glass:hover { background: rgba(255, 255, 255, 0.12); }
    .btn-primary {
      background: linear-gradient(135deg, #2563eb, #0ea5e9);
      color: #fff;
      box-shadow: 0 4px 14px var(--primary-glow);
    }
    .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 20px var(--primary-glow); }

    /* ==========================================================================
       6. DUPLICATE DETECTION FLOATING GLASS MODAL
       ========================================================================== */
    .dup-modal-overlay {
      position: absolute;
      inset: 0;
      z-index: 700;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .dup-modal-overlay.open { display: flex; }
    .dup-card {
      width: 440px;
      max-width: 90vw;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid var(--warning);
      border-radius: var(--radius-xl);
      padding: 24px;
      box-shadow: 0 0 35px rgba(245, 158, 11, 0.35);
      animation: panelSlideIn 0.25s ease;
    }
    .dup-header { display: flex; align-items: center; gap: 10px; color: var(--warning); font-size: 16px; font-weight: 800; margin-bottom: 8px; }
    .dup-card p { font-size: 13px; color: var(--text-muted); line-height: 1.5; margin-bottom: 16px; }
    .dup-existing-box {
      background: rgba(0,0,0,0.35);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      padding: 12px;
      margin-bottom: 18px;
    }
    .dup-existing-box h5 { font-size: 13px; font-weight: 700; color: #fff; }
    .dup-existing-box p { font-size: 11.5px; color: var(--text-muted); margin-top: 4px; }

    /* ==========================================================================
       7. ADMIN & OFFICER FLOATING GLASS DRAWERS / PANELS
       ========================================================================== */
    .floating-side-drawer {
      position: absolute;
      top: 94px;
      right: 24px;
      width: 520px;
      max-width: calc(100vw - 48px);
      max-height: calc(100vh - 120px);
      z-index: 550;
      background: rgba(13, 20, 38, 0.85);
      backdrop-filter: blur(24px) saturate(190%);
      border: 1px solid var(--glass-border-light);
      border-radius: var(--radius-xl);
      box-shadow: var(--glass-shadow);
      display: none;
      flex-direction: column;
      overflow: hidden;
      animation: drawerSlide 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .floating-side-drawer.open { display: flex; }
    @keyframes drawerSlide {
      from { opacity: 0; transform: translateX(30px); }
      to { opacity: 1; transform: translateX(0); }
    }

    /* KPI Grid */
    .kpi-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 16px;
    }
    .kpi-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      padding: 12px 10px;
      text-align: center;
    }
    .kpi-val { font-size: 20px; font-weight: 900; line-height: 1.1; }
    .kpi-label { font-size: 10px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); margin-top: 4px; }

    /* Table within Glass Panel */
    .glass-table-wrap {
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      overflow: hidden;
      background: rgba(0, 0, 0, 0.25);
    }
    table { width: 100%; border-collapse: collapse; }
    th {
      text-align: left;
      padding: 10px 14px;
      font-size: 10.5px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      border-bottom: 1px solid var(--glass-border);
      background: rgba(0,0,0,0.2);
    }
    td {
      padding: 12px 14px;
      font-size: 12.5px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      vertical-align: middle;
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: rgba(255, 255, 255, 0.03); }

    /* Status Badges */
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 9px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 800;
    }
    .pill-reported { background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border: 1px solid #64748b; }
    .pill-verified { background: rgba(59, 130, 246, 0.18); color: #93c5fd; border: 1px solid var(--primary); }
    .pill-assigned { background: rgba(245, 158, 11, 0.18); color: #fde68a; border: 1px solid var(--warning); }
    .pill-progress { background: rgba(168, 85, 247, 0.18); color: #e9d5ff; border: 1px solid var(--purple); }
    .pill-resolved { background: rgba(16, 185, 129, 0.18); color: #a7f3d0; border: 1px solid var(--success); }

    /* Priority Pills */
    .p-badge { padding: 2px 7px; border-radius: 4px; font-size: 10.5px; font-weight: 800; }
    .p-P1 { background: rgba(239, 68, 68, 0.25); color: #fca5a5; border: 1px solid var(--danger); }
    .p-P2 { background: rgba(245, 158, 11, 0.25); color: #fde68a; border: 1px solid var(--warning); }
    .p-P3 { background: rgba(59, 130, 246, 0.25); color: #93c5fd; border: 1px solid var(--primary); }
    .p-P4 { background: rgba(16, 185, 129, 0.25); color: #a7f3d0; border: 1px solid var(--success); }

    /* ==========================================================================
       8. CUSTOM GLOWING MAP MARKERS & POPUP CARD
       ========================================================================== */
    .pulse-marker-beacon {
      position: relative;
      width: 22px;
      height: 22px;
    }
    .beacon-core {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      position: absolute;
      top: 4px;
      left: 4px;
      border: 2px solid #fff;
      box-shadow: 0 0 10px rgba(0,0,0,0.8);
      z-index: 2;
    }
    .beacon-wave {
      position: absolute;
      top: 0;
      left: 0;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      opacity: 0.8;
      animation: beaconRipple 2s infinite ease-out;
      z-index: 1;
    }
    @keyframes beaconRipple {
      0% { transform: scale(0.6); opacity: 1; }
      100% { transform: scale(2.4); opacity: 0; }
    }

    /* Leaflet Popup customization */
    .leaflet-popup-content-wrapper {
      background: rgba(15, 23, 42, 0.92) !important;
      color: #fff !important;
      backdrop-filter: blur(16px);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md) !important;
      box-shadow: var(--glass-shadow) !important;
      padding: 0 !important;
    }
    .leaflet-popup-content { margin: 16px !important; min-width: 220px; font-family: inherit; }
    .leaflet-popup-tip { background: rgba(15, 23, 42, 0.92) !important; }

    /* ==========================================================================
       9. TOAST NOTIFICATIONS
       ========================================================================== */
    #toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .toast-card {
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(16px);
      border: 1px solid var(--glass-border);
      border-left: 4px solid var(--primary);
      border-radius: 12px;
      padding: 12px 18px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
      box-shadow: var(--glass-shadow);
      display: flex;
      align-items: center;
      gap: 12px;
      animation: toastIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      min-width: 280px;
    }
    .toast-card.success { border-left-color: var(--success); }
    .toast-card.warning { border-left-color: var(--warning); }
    .toast-card.danger { border-left-color: var(--danger); }
    @keyframes toastIn { from { opacity: 0; transform: translateX(50px); } to { opacity: 1; transform: translateX(0); } }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 10px; }
  </style>
</head>
<body>

  <!-- ==========================================================================
       1. HERO MAP CANVAS
       ========================================================================== -->
  <div id="map-viewport">
    <div id="map"></div>
  </div>

  <!-- ==========================================================================
       2. TOP FLOATING NAVIGATION
       ========================================================================== -->
  <nav id="top-nav">
    <div class="brand-section" onclick="flyToCityCenter()">
      <div class="brand-logo-badge"><i class="fa-solid fa-bridge-water"></i></div>
      <div class="brand-title-wrap">
        <h1>INFRA<span>care</span></h1>
        <p>Building Better Cities Together</p>
      </div>
    </div>

    <!-- Center Nav Pills -->
    <div class="nav-pills">
      <button class="nav-pill active" id="btn-nav-map" onclick="activateNavTab('map')">
        <i class="fa-solid fa-earth-asia"></i> Live Map
      </button>
      <button class="nav-pill report-btn" id="btn-nav-report" onclick="openReportPanel()">
        <i class="fa-solid fa-circle-plus"></i> Report Issue
      </button>
      <button class="nav-pill" id="btn-nav-records" onclick="activateNavTab('records')">
        <i class="fa-solid fa-list-check"></i> Incidents
      </button>
      <button class="nav-pill" id="btn-nav-admin" onclick="activateNavTab('admin')">
        <i class="fa-solid fa-chart-line"></i> Admin Analytics
      </button>
      <button class="nav-pill" id="btn-nav-officer" onclick="activateNavTab('officer')">
        <i class="fa-solid fa-route"></i> Officer Route
      </button>
    </div>

    <!-- Right Controls -->
    <div class="nav-right-actions">
      <div class="icon-action-btn" onclick="checkNotifications()" title="Notifications">
        <i class="fa-regular fa-bell"></i>
        <span class="badge-dot" id="notif-badge" style="display:none;">0</span>
      </div>

      <div class="role-badge-select">
        <div class="role-avatar" id="role-avatar">C</div>
        <select class="role-dropdown" id="role-select" onchange="onRoleChange(this.value)">
          <option value="citizen">Citizen Demo</option>
          <option value="admin">Municipal Admin</option>
          <option value="officer">Field Officer</option>
        </select>
      </div>
    </div>
  </nav>

  <!-- ==========================================================================
       3. MAP SEARCH BAR & LAYER SWITCHER
       ========================================================================== -->
  <div class="map-search-bar">
    <i class="fa-solid fa-magnifying-glass" style="color:var(--text-muted); font-size:14px;"></i>
    <input type="text" id="map-search-input" placeholder="Search location, road or pincode in Delhi..." onkeydown="handleMapSearch(event)" />
    <i class="fa-solid fa-crosshairs" onclick="locateUserGPS()" style="color:var(--primary); cursor:pointer; font-size:14px;" title="Find My Location"></i>
  </div>

  <div class="map-layer-selector">
    <button class="layer-toggle-btn active" id="layer-sat-btn" onclick="toggleMapLayer('satellite')">
      <i class="fa-solid fa-satellite"></i> Satellite
    </button>
    <button class="layer-toggle-btn" id="layer-str-btn" onclick="toggleMapLayer('street')">
      <i class="fa-solid fa-map"></i> Street
    </button>
  </div>

  <!-- Right Vertical Toolbar -->
  <div class="map-vertical-toolbar">
    <div class="toolbar-tool-btn" onclick="locateUserGPS()">
      <i class="fa-solid fa-location-crosshairs"></i>
      <span class="toolbar-tooltip">My Location</span>
    </div>
    <div class="toolbar-tool-btn" onclick="toggleHotspots()" id="btn-hotspots">
      <i class="fa-solid fa-fire-flame-curved"></i>
      <span class="toolbar-tooltip">Damage Hotspots</span>
    </div>
    <div class="toolbar-tool-btn" onclick="filterBySeverity('Critical')" id="btn-filter-crit">
      <i class="fa-solid fa-triangle-exclamation" style="color:var(--danger)"></i>
      <span class="toolbar-tooltip">Critical Issues</span>
    </div>
    <div class="toolbar-tool-btn" onclick="syncAllData()">
      <i class="fa-solid fa-arrows-rotate"></i>
      <span class="toolbar-tooltip">Sync Live Data</span>
    </div>
    <div class="toolbar-tool-btn" onclick="toggleFullscreen()">
      <i class="fa-solid fa-expand"></i>
      <span class="toolbar-tooltip">Fullscreen Map</span>
    </div>
  </div>

  <!-- Bottom Legend -->
  <div class="map-priority-legend">
    <div class="legend-item"><span class="legend-beacon beacon-critical"></span> Critical (P1)</div>
    <div class="legend-item"><span class="legend-beacon beacon-high"></span> High (P2)</div>
    <div class="legend-item"><span class="legend-beacon beacon-medium"></span> Medium (P3)</div>
    <div class="legend-item"><span class="legend-beacon beacon-low"></span> Low (P4)</div>
  </div>

  <!-- ==========================================================================
       4. FLOATING 3-STEP REPORT GLASS PANEL
       ========================================================================== -->
  <div id="report-glass-panel">
    <div class="panel-header">
      <div class="panel-header-info">
        <h2><i class="fa-solid fa-map-pin" style="color:var(--primary);"></i> Report Damage</h2>
        <p>Help municipal authorities fix public infrastructure</p>
      </div>
      <button class="panel-close-btn" onclick="closeReportPanel()"><i class="fa-solid fa-xmark"></i></button>
    </div>

    <!-- Stepper indicator -->
    <div class="stepper-wrap">
      <div class="step-node active" id="step-node-1" onclick="jumpToStep(1)">
        <div class="step-circle">1</div>
        <div class="step-title">Details</div>
      </div>
      <div class="step-connector"></div>
      <div class="step-node" id="step-node-2" onclick="jumpToStep(2)">
        <div class="step-circle">2</div>
        <div class="step-title">Location</div>
      </div>
      <div class="step-connector"></div>
      <div class="step-node" id="step-node-3" onclick="jumpToStep(3)">
        <div class="step-circle">3</div>
        <div class="step-title">Review</div>
      </div>
    </div>

    <!-- Body Steps -->
    <div class="panel-body">
      <!-- STEP 1: Details & Photo -->
      <div class="form-step-content active" id="step-content-1">
        <label class="field-label">1. Asset Category</label>
        <div class="cat-grid">
          <div class="cat-card selected" data-cat="Road" onclick="selectCategory('Road', this)">
            <div class="cat-icon">🛣️</div>
            <div class="cat-label">
              <h4>Road & Pothole</h4>
              <p>Asphalt, crater, divider</p>
            </div>
          </div>
          <div class="cat-card" data-cat="Bridge" onclick="selectCategory('Bridge', this)">
            <div class="cat-icon">🌉</div>
            <div class="cat-label">
              <h4>Bridge / Flyover</h4>
              <p>Expansion joints, cracks</p>
            </div>
          </div>
          <div class="cat-card" data-cat="Lighting" onclick="selectCategory('Lighting', this)">
            <div class="cat-icon">💡</div>
            <div class="cat-label">
              <h4>Street Lighting</h4>
              <p>Blackout, wiring, pole</p>
            </div>
          </div>
          <div class="cat-card" data-cat="Other" onclick="selectCategory('Other', this)">
            <div class="cat-icon">🏗️</div>
            <div class="cat-label">
              <h4>Other Public Asset</h4>
              <p>Drainage, signages</p>
            </div>
          </div>
        </div>

        <label class="field-label">2. Severity Level</label>
        <div class="severity-row">
          <div class="sev-chip" data-sev="Low" onclick="selectSeverity('Low', this)">🟢 Low</div>
          <div class="sev-chip" data-sev="Medium" onclick="selectSeverity('Medium', this)">🟡 Medium</div>
          <div class="sev-chip selected" data-sev="High" onclick="selectSeverity('High', this)">🟠 High</div>
          <div class="sev-chip" data-sev="Critical" onclick="selectSeverity('Critical', this)">🔴 Critical</div>
        </div>

        <div class="field-group">
          <label class="field-label">3. Incident Title *</label>
          <input type="text" id="report-title-input" class="glass-input" placeholder="e.g., Deep crater pothole causing bike skids" required />
        </div>

        <div class="field-group">
          <label class="field-label">4. Damage Description *</label>
          <textarea id="report-desc-input" class="glass-textarea" placeholder="Describe depth, traffic disruption, lane blockage, or safety risks in detail..." required></textarea>
        </div>

        <div class="field-group">
          <label class="field-label">5. Damage Photo (Recommended)</label>
          <div class="upload-zone" id="photo-dropzone" onclick="document.getElementById('photo-file-input').click()">
            <div class="upload-icon"><i class="fa-solid fa-cloud-arrow-up"></i></div>
            <h4>Upload or Drag Damage Photo</h4>
            <p>PNG, JPG, WebP • Max 5.0 MB</p>
            <input type="file" id="photo-file-input" accept="image/png, image/jpeg, image/webp" style="display:none;" onchange="handlePhotoSelected(this)" />
          </div>

          <div class="photo-preview-card" id="photo-preview-box">
            <img class="photo-thumb" id="preview-img-tag" src="" alt="Damage Preview" />
            <div class="photo-meta">
              <div class="photo-name" id="preview-filename">damage.jpg</div>
              <div class="photo-size" id="preview-filesize">1.4 MB</div>
            </div>
            <button type="button" class="photo-remove-btn" onclick="removePhoto()"><i class="fa-solid fa-trash"></i> Remove</button>
          </div>
        </div>
      </div>

      <!-- STEP 2: Interactive Location -->
      <div class="form-step-content" id="step-content-2">
        <div class="loc-action-card">
          <p style="font-size:12.5px; color:var(--text-muted); margin-bottom:12px;">
            Click anywhere on the satellite map or use automatic GPS to pinpoint the exact location.
          </p>
          <button type="button" class="gps-btn" id="btn-gps-acquire" onclick="acquireLocationGPS()">
            <i class="fa-solid fa-location-arrow"></i> Use My Current Location
          </button>
        </div>

        <div class="coords-display-box">
          <div class="coords-row">
            <span style="color:var(--text-muted)">Latitude:</span>
            <span class="coords-val" id="coords-lat-val">28.63150</span>
          </div>
          <div class="coords-row">
            <span style="color:var(--text-muted)">Longitude:</span>
            <span class="coords-val" id="coords-lng-val">77.21670</span>
          </div>
          <div class="coords-row" style="margin-top:6px; border-top:1px dashed var(--glass-border); padding-top:6px;">
            <span style="color:var(--text-muted)">Geocoded Landmark:</span>
            <span style="color:#fff; font-size:11px;" id="coords-landmark-val">Connaught Place, New Delhi</span>
          </div>
        </div>

        <p style="font-size:11.5px; color:var(--accent-cyan); margin-top:14px; text-align:center;">
          <i class="fa-solid fa-hand-pointer"></i> Tip: You can drag the red marker directly on the satellite map!
        </p>
      </div>

      <!-- STEP 3: Review & AI Priority -->
      <div class="form-step-content" id="step-content-3">
        <div class="review-summary-card">
          <div class="review-item">
            <span class="review-label">Category:</span>
            <span class="review-val" id="rev-cat">Road & Pothole</span>
          </div>
          <div class="review-item">
            <span class="review-label">Severity:</span>
            <span class="review-val" id="rev-sev">High</span>
          </div>
          <div class="review-item">
            <span class="review-label">Title:</span>
            <span class="review-val" id="rev-title">—</span>
          </div>
          <div class="review-item">
            <span class="review-label">Coordinates:</span>
            <span class="review-val" id="rev-coords">28.63150, 77.21670</span>
          </div>
          <div class="review-item">
            <span class="review-label">Photo Attached:</span>
            <span class="review-val" id="rev-photo-status">No photo</span>
          </div>
        </div>

        <div class="ai-priority-box">
          <div class="ai-priority-icon"><i class="fa-solid fa-bolt-lightning"></i></div>
          <div class="ai-priority-info">
            <h4 id="computed-priority-title">Estimated Priority: P1 Critical</h4>
            <p id="computed-priority-reason">Calculated by road safety impact formula and category weight.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Progress overlay during submission -->
    <div class="submit-progress-overlay" id="submit-overlay">
      <div class="spinner-ring" id="sub-spinner"></div>
      <div class="success-badge-icon" id="sub-success-icon" style="display:none;"><i class="fa-solid fa-check"></i></div>
      <div class="progress-step-txt" id="sub-step-msg">Uploading damage report...</div>
      <div class="progress-sub-txt" id="sub-step-sub">Checking duplicate database & calculating priority</div>
      <button class="btn btn-primary" id="btn-sub-done" style="display:none; margin-top:16px;" onclick="closeReportPanel()">View on Live Map</button>
    </div>

    <!-- Footer Actions -->
    <div class="panel-footer">
      <button class="btn btn-glass" id="btn-step-prev" onclick="goToPreviousStep()" style="visibility:hidden;">
        <i class="fa-solid fa-arrow-left"></i> Back
      </button>
      <button class="btn btn-primary" id="btn-step-next" onclick="goToNextStep()">
        Next: Choose Location <i class="fa-solid fa-arrow-right"></i>
      </button>
    </div>
  </div>

  <!-- ==========================================================================
       5. DUPLICATE DETECTION MODAL
       ========================================================================== -->
  <div class="dup-modal-overlay" id="duplicate-modal">
    <div class="dup-card">
      <div class="dup-header">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <span>Similar Incident Found Nearby</span>
      </div>
      <p>We found an existing verified damage report within 50 meters of your pinned coordinates.</p>
      
      <div class="dup-existing-box">
        <h5 id="dup-report-title">Large Asphalt Crater on Main Road</h5>
        <p id="dup-report-meta">Category: Road • Priority: P1 • 8 Community Votes</p>
      </div>

      <div style="display:flex; flex-direction:column; gap:8px;">
        <button class="btn btn-primary" onclick="supportDuplicateReport()">
          <i class="fa-solid fa-thumbs-up"></i> Support Existing Issue (+1 Vote)
        </button>
        <button class="btn btn-glass" onclick="submitAsSeparateReport()">
          Submit As Separate Incident
        </button>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       6. INCIDENT RECORDS DRAWER (CITIZEN / ADMIN)
       ========================================================================== -->
  <div class="floating-side-drawer" id="drawer-records">
    <div class="panel-header">
      <div class="panel-header-info">
        <h2><i class="fa-solid fa-list-check" style="color:var(--primary);"></i> Infrastructure Incidents</h2>
        <p>Live municipal damage feed and citizen tracking</p>
      </div>
      <button class="panel-close-btn" onclick="closeAllDrawers()"><i class="fa-solid fa-xmark"></i></button>
    </div>
    <div class="panel-body">
      <div class="glass-table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Category</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="incidents-table-body"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       7. ADMIN ANALYTICS DRAWER
       ========================================================================== -->
  <div class="floating-side-drawer" id="drawer-admin">
    <div class="panel-header">
      <div class="panel-header-info">
        <h2><i class="fa-solid fa-chart-pie" style="color:var(--accent-cyan);"></i> Municipal Operations Overview</h2>
        <p>City-wide infrastructure KPIs & SLA performance</p>
      </div>
      <button class="panel-close-btn" onclick="closeAllDrawers()"><i class="fa-solid fa-xmark"></i></button>
    </div>
    <div class="panel-body">
      <div class="kpi-row">
        <div class="kpi-card">
          <div class="kpi-val" id="kpi-total" style="color:var(--primary);">0</div>
          <div class="kpi-label">Total Reports</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" id="kpi-pending" style="color:var(--warning);">0</div>
          <div class="kpi-label">Active Pending</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" id="kpi-resolved" style="color:var(--success);">0</div>
          <div class="kpi-label">Resolved</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" id="kpi-crit" style="color:var(--danger);">0</div>
          <div class="kpi-label">Critical P1</div>
        </div>
      </div>

      <h4 style="font-size:13px; font-weight:800; margin:16px 0 8px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.04em;">
        Incident Dispatch & Verification Queue
      </h4>
      <div class="glass-table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Incident</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Manage</th>
            </tr>
          </thead>
          <tbody id="admin-queue-body"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       8. OFFICER ROUTE DRAWER
       ========================================================================== -->
  <div class="floating-side-drawer" id="drawer-officer">
    <div class="panel-header">
      <div class="panel-header-info">
        <h2><i class="fa-solid fa-route" style="color:var(--accent-teal);"></i> Field Inspection Route</h2>
        <p>OR-Tools Optimized Inspection & Repair Sequence</p>
      </div>
      <button class="panel-close-btn" onclick="closeAllDrawers()"><i class="fa-solid fa-xmark"></i></button>
    </div>
    <div class="panel-body">
      <button class="btn btn-primary" style="width:100%; margin-bottom:16px;" onclick="renderOptimizedOfficerRoute()">
        <i class="fa-solid fa-wand-magic-sparkles"></i> Calculate Nearest-Neighbor Route
      </button>

      <div class="glass-table-wrap">
        <table>
          <thead>
            <tr>
              <th>Stop</th>
              <th>Incident</th>
              <th>Severity</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="officer-route-body"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Toast Wrap -->
  <div id="toast-container"></div>

  <!-- ==========================================================================
       JAVASCRIPT LOGIC & INTERACTIONS
       ========================================================================== -->
  <script>
    const API_BASE = '/api';
    const ESRI_SATELLITE_URL = 'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
    const OSM_STREET_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

    // State
    let map, satLayer, strLayer;
    let currentTileLayer = 'satellite';
    let reportsData = [];
    let markersGroup = L.layerGroup();
    let hotspotLayer = L.layerGroup();
    let routePolyline = null;
    let selectedPinMarker = null;
    let currentStep = 1;
    let selectedCategory = 'Road';
    let selectedSeverity = 'High';
    let currentLat = 28.63150;
    let currentLng = 77.21670;
    let selectedPhotoFile = null;
    let detectedDuplicateId = null;
    let currentRole = 'citizen';

    // ── INITIALIZATION ────────────────────────────────────────────────────────
    window.addEventListener('DOMContentLoaded', () => {
      initMap();
      syncAllData();
      checkNotifications();
      setInterval(checkNotifications, 15000);
    });

    function initMap() {
      // Centered on Central Delhi (Connaught Place) for vivid SIH demo
      map = L.map('map', { zoomControl: false }).setView([28.63150, 77.21670], 14);

      satLayer = L.tileLayer(ESRI_SATELLITE_URL, { maxZoom: 19, attribution: 'Imagery © Esri' });
      strLayer = L.tileLayer(OSM_STREET_URL, { maxZoom: 19, attribution: '© OpenStreetMap' });

      satLayer.addTo(map);
      markersGroup.addTo(map);
      hotspotLayer.addTo(map);

      // Move zoom controls bottom right
      L.control.zoom({ position: 'bottomright' }).addTo(map);

      // Map Click for Location Selection
      map.on('click', (e) => {
        if (document.getElementById('report-glass-panel').classList.contains('open')) {
          updatePinnedLocation(e.latlng.lat, e.latlng.lng);
        }
      });
    }

    function toggleMapLayer(layer) {
      currentTileLayer = layer;
      if (layer === 'satellite') {
        map.removeLayer(strLayer);
        satLayer.addTo(map);
        document.getElementById('layer-sat-btn').classList.add('active');
        document.getElementById('layer-str-btn').classList.remove('active');
      } else {
        map.removeLayer(satLayer);
        strLayer.addTo(map);
        document.getElementById('layer-str-btn').classList.add('active');
        document.getElementById('layer-sat-btn').classList.remove('active');
      }
    }

    function flyToCityCenter() {
      map.flyTo([28.63150, 77.21670], 14, { duration: 1.5 });
    }

    // ── USER GPS & RADAR ANIMATION ───────────────────────────────────────────
    async function locateUserGPS() {
      const gpsBtn = document.getElementById('btn-gps-acquire');
      if (gpsBtn) gpsBtn.classList.add('locating');
      showToast('Finding your exact location (GPS / WiFi)...', 'info');

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          async (pos) => {
            const lat = pos.coords.latitude;
            const lng = pos.coords.longitude;
            if (gpsBtn) gpsBtn.classList.remove('locating');
            
            // Smooth Camera FlyTo
            map.flyTo([lat, lng], 17, { duration: 1.8, easeLinearity: 0.25 });
            
            // Radar pulse circle
            const radarCircle = L.circle([lat, lng], {
              radius: pos.coords.accuracy || 35,
              color: '#06b6d4',
              fillColor: '#3b82f6',
              fillOpacity: 0.25,
              weight: 2
            }).addTo(map);
            setTimeout(() => map.removeLayer(radarCircle), 3500);

            await updatePinnedLocation(lat, lng);
            showToast(`Location acquired: ${lat.toFixed(4)}, ${lng.toFixed(4)}`, 'success');
          },
          async (err) => {
            console.warn('Browser GPS error or denied, trying IP geolocation fallback...', err);
            await fallbackIpLocation(gpsBtn);
          },
          { enableHighAccuracy: true, timeout: 7000, maximumAge: 10000 }
        );
      } else {
        await fallbackIpLocation(gpsBtn);
      }
    }

    const acquireLocationGPS = locateUserGPS;

    async function fallbackIpLocation(gpsBtn) {
      try {
        const res = await fetch('https://ipwho.is/');
        const data = await res.json();
        if (gpsBtn) gpsBtn.classList.remove('locating');
        if (data.success && data.latitude && data.longitude) {
          const lat = data.latitude;
          const lng = data.longitude;
          map.flyTo([lat, lng], 15, { duration: 1.8 });
          await updatePinnedLocation(lat, lng, data.city + ', ' + data.region);
          showToast(`Location detected (${data.city}, ${data.region})`, 'success');
          return;
        }
      } catch(e) {}
      if (gpsBtn) gpsBtn.classList.remove('locating');
      // Default to Delhi central coordinates
      map.flyTo([28.6315, 77.2167], 15, { duration: 1.5 });
      await updatePinnedLocation(28.6315, 77.2167, 'Connaught Place, New Delhi');
      showToast('Set to central demo location (click map to change)', 'info');
    }

    async function updatePinnedLocation(lat, lng, customLandmark = null) {
      currentLat = lat;
      currentLng = lng;
      document.getElementById('coords-lat-val').textContent = lat.toFixed(5);
      document.getElementById('coords-lng-val').textContent = lng.toFixed(5);
      document.getElementById('rev-coords').textContent = `${lat.toFixed(5)}, ${lng.toFixed(5)}`;

      if (customLandmark) {
        document.getElementById('coords-landmark-val').textContent = customLandmark;
      } else {
        // Reverse geocode asynchronously
        reverseGeocode(lat, lng);
      }

      if (selectedPinMarker) map.removeLayer(selectedPinMarker);

      // Draggable glowing Leaflet marker
      const pinIcon = L.divIcon({
        className: 'custom-pin',
        html: `<div class="pulse-marker-beacon">
                 <div class="beacon-wave" style="background:var(--danger)"></div>
                 <div class="beacon-core" style="background:var(--danger)"></div>
               </div>`,
        iconSize: [22, 22],
        iconAnchor: [11, 11]
      });

      selectedPinMarker = L.marker([lat, lng], { icon: pinIcon, draggable: true }).addTo(map);
      selectedPinMarker.on('dragend', async (ev) => {
        const pt = ev.target.getLatLng();
        await updatePinnedLocation(pt.lat, pt.lng);
        showToast(`Pinned at ${pt.lat.toFixed(4)}, ${pt.lng.toFixed(4)}`, 'info');
      });
    }

    async function reverseGeocode(lat, lng) {
      try {
        const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=16`);
        if (res.ok) {
          const data = await res.json();
          const name = data.display_name ? data.display_name.split(',').slice(0, 3).join(', ') : 'Detected GIS Location';
          document.getElementById('coords-landmark-val').textContent = name;
        }
      } catch(e) {
        document.getElementById('coords-landmark-val').textContent = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
      }
    }

    // ── DATA SYNC & MAP MARKERS ──────────────────────────────────────────────
    async function syncAllData() {
      try {
        const res = await fetch(`${API_BASE}/reports`);
        if (!res.ok) throw new Error();
        reportsData = await res.json();
        renderMapMarkers();
        renderIncidentsTable();
        renderAdminDashboard();
        renderOfficerTasks();
        showToast('Live infrastructure data synced', 'success');
      } catch (err) {
        showToast('Connecting to backend API...', 'info');
      }
    }

    function renderMapMarkers() {
      markersGroup.clearLayers();
      hotspotLayer.clearLayers();

      const colorMap = {
        Critical: '#ef4444',
        High: '#f59e0b',
        Medium: '#06b6d4',
        Low: '#10b981'
      };

      reportsData.forEach(r => {
        const color = colorMap[r.severity] || '#3b82f6';
        const icon = L.divIcon({
          className: 'custom-marker',
          html: `
            <div class="pulse-marker-beacon">
              <div class="beacon-wave" style="background:${color}"></div>
              <div class="beacon-core" style="background:${color}"></div>
            </div>
          `,
          iconSize: [22, 22],
          iconAnchor: [11, 11]
        });

        const marker = L.marker([r.latitude, r.longitude], { icon });

        // Glass Popup Card
        const photoHtml = r.image_url ? `<img src="${r.image_url}" style="width:100%; height:110px; object-fit:cover; border-radius:8px; margin-bottom:10px;" />` : '';
        marker.bindPopup(`
          <div>
            ${photoHtml}
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
              <span class="p-badge p-${r.priority || 'P3'}">${r.priority || 'P3'}</span>
              <span class="pill pill-${(r.status||'reported').toLowerCase()}">${r.status}</span>
            </div>
            <h4 style="font-size:14px; font-weight:800; margin-bottom:4px;">${esc(r.title)}</h4>
            <p style="font-size:11.5px; color:#94a3b8; line-height:1.4; margin-bottom:10px;">${esc(r.description || '')}</p>
            <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(255,255,255,0.1); padding-top:8px;">
              <span style="font-size:11px; font-weight:700;">👍 ${r.support_count || 0} Votes</span>
              <button onclick="supportReport(${r.id})" style="background:var(--primary); color:#fff; border:none; border-radius:6px; padding:4px 10px; font-size:11px; font-weight:700; cursor:pointer;">Support</button>
            </div>
          </div>
        `);
        markersGroup.addLayer(marker);

        // Density circle for hotspots
        if (r.severity === 'Critical' || (r.support_count || 0) > 5) {
          const circle = L.circle([r.latitude, r.longitude], {
            radius: 75,
            color: '#ef4444',
            fillColor: '#ef4444',
            fillOpacity: 0.15,
            weight: 1
          });
          hotspotLayer.addLayer(circle);
        }
      });
    }

    // ── 3-STEP REPORT PANEL LOGIC ─────────────────────────────────────────────
    function openReportPanel() {
      closeAllDrawers();
      document.getElementById('report-glass-panel').classList.add('open');
      document.getElementById('duplicate-modal').classList.remove('open');
      jumpToStep(1);
      if (!selectedPinMarker) {
        updatePinnedLocation(currentLat, currentLng);
      }
    }
    function closeReportPanel() {
      document.getElementById('report-glass-panel').classList.remove('open');
      if (selectedPinMarker) {
        map.removeLayer(selectedPinMarker);
        selectedPinMarker = null;
      }
    }

    function jumpToStep(step) {
      currentStep = step;
      document.querySelectorAll('.form-step-content').forEach(s => s.classList.remove('active'));
      document.querySelectorAll('.step-node').forEach((node, idx) => {
        node.classList.remove('active', 'completed');
        if (idx + 1 === step) node.classList.add('active');
        if (idx + 1 < step) node.classList.add('completed');
      });

      document.getElementById(`step-content-${step}`).classList.add('active');

      const prevBtn = document.getElementById('btn-step-prev');
      const nextBtn = document.getElementById('btn-step-next');

      if (step === 1) {
        prevBtn.style.visibility = 'hidden';
        nextBtn.innerHTML = 'Next: Choose Location <i class="fa-solid fa-arrow-right"></i>';
      } else if (step === 2) {
        prevBtn.style.visibility = 'visible';
        nextBtn.innerHTML = 'Next: Review & Submit <i class="fa-solid fa-arrow-right"></i>';
      } else if (step === 3) {
        prevBtn.style.visibility = 'visible';
        nextBtn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Submit Incident Report';
        updateReviewSummary();
      }
    }

    function goToNextStep() {
      if (currentStep === 1) {
        const title = document.getElementById('report-title-input').value.trim();
        const desc = document.getElementById('report-desc-input').value.trim();
        if (!title || !desc) {
          showToast('Please enter an incident title and description', 'warning');
          return;
        }
        jumpToStep(2);
      } else if (currentStep === 2) {
        jumpToStep(3);
      } else if (currentStep === 3) {
        executeReportSubmission();
      }
    }

    function goToPreviousStep() {
      if (currentStep > 1) jumpToStep(currentStep - 1);
    }

    function selectCategory(cat, el) {
      selectedCategory = cat;
      document.querySelectorAll('.cat-card').forEach(c => c.classList.remove('selected'));
      el.classList.add('selected');
    }
    function selectSeverity(sev, el) {
      selectedSeverity = sev;
      document.querySelectorAll('.sev-chip').forEach(c => c.classList.remove('selected'));
      el.classList.add('selected');
    }

    // Photo Handler
    function handlePhotoSelected(input) {
      if (!input.files || !input.files[0]) return;
      const file = input.files[0];

      if (file.size > 5 * 1024 * 1024) {
        showToast('Image exceeds 5MB limit. Please choose a smaller photo.', 'danger');
        input.value = '';
        return;
      }

      selectedPhotoFile = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        document.getElementById('preview-img-tag').src = e.target.result;
        document.getElementById('preview-filename').textContent = file.name;
        document.getElementById('preview-filesize').textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB';
        document.getElementById('photo-preview-box').classList.add('show');
        document.getElementById('photo-dropzone').style.display = 'none';
      };
      reader.readAsDataURL(file);
    }

    function removePhoto() {
      selectedPhotoFile = null;
      document.getElementById('photo-file-input').value = '';
      document.getElementById('photo-preview-box').classList.remove('show');
      document.getElementById('photo-dropzone').style.display = 'block';
    }

    function updateReviewSummary() {
      document.getElementById('rev-cat').textContent = selectedCategory;
      document.getElementById('rev-sev').textContent = selectedSeverity;
      document.getElementById('rev-title').textContent = document.getElementById('report-title-input').value || '—';
      document.getElementById('rev-coords').textContent = `${currentLat.toFixed(5)}, ${currentLng.toFixed(5)}`;
      document.getElementById('rev-photo-status').textContent = selectedPhotoFile ? `✓ ${selectedPhotoFile.name}` : 'No photo attached';

      // Computed priority preview
      const prio = selectedSeverity === 'Critical' ? 'P1 Critical' : selectedSeverity === 'High' ? 'P2 High' : 'P3 Medium';
      document.getElementById('computed-priority-title').textContent = `Computed AI Priority: ${prio}`;
    }

    // ── SUBMISSION FLOW WITH PROGRESS ANIMATION ───────────────────────────────
    async function executeReportSubmission() {
      const overlay = document.getElementById('submit-overlay');
      const stepMsg = document.getElementById('sub-step-msg');
      const stepSub = document.getElementById('sub-step-sub');
      const spinner = document.getElementById('sub-spinner');
      const successIcon = document.getElementById('sub-success-icon');
      const doneBtn = document.getElementById('btn-sub-done');

      overlay.classList.add('show');
      spinner.style.display = 'block';
      successIcon.style.display = 'none';
      doneBtn.style.display = 'none';

      stepMsg.textContent = '1/4: Uploading damage telemetry & photo...';
      await delay(400);

      stepMsg.textContent = '2/4: Verifying GIS spatial coordinates...';
      await delay(350);

      stepMsg.textContent = '3/4: Querying duplicate radar database...';

      const fd = new FormData();
      fd.append('title', document.getElementById('report-title-input').value.trim());
      fd.append('description', document.getElementById('report-desc-input').value.trim());
      fd.append('category', selectedCategory);
      fd.append('severity', selectedSeverity);
      fd.append('latitude', currentLat);
      fd.append('longitude', currentLng);
      if (selectedPhotoFile) fd.append('image', selectedPhotoFile);

      try {
        const res = await fetch(`${API_BASE}/reports`, { method: 'POST', body: fd });
        const data = await res.json();

        if (data.is_duplicate || data.duplicate_of_id) {
          overlay.classList.remove('show');
          detectedDuplicateId = data.duplicate_of_id;
          document.getElementById('duplicate-modal').classList.add('open');
          return;
        }

        stepMsg.textContent = '4/4: Calculating city-wide priority index...';
        await delay(350);

        spinner.style.display = 'none';
        successIcon.style.display = 'flex';
        stepMsg.textContent = `Incident Submitted! 🎉 IC-#${data.id}`;
        stepSub.textContent = `Assigned Priority: ${data.priority || 'P1'} • Dispatch Status: Reported`;
        doneBtn.style.display = 'inline-flex';

        // Reset inputs
        document.getElementById('report-title-input').value = '';
        document.getElementById('report-desc-input').value = '';
        removePhoto();
        syncAllData();
      } catch (err) {
        overlay.classList.remove('show');
        showToast('Error connecting to backend database', 'danger');
      }
    }

    // ── DUPLICATE RESOLUTION ──────────────────────────────────────────────────
    async function supportDuplicateReport() {
      if (!detectedDuplicateId) return;
      await supportReport(detectedDuplicateId);
      document.getElementById('duplicate-modal').classList.remove('open');
      closeReportPanel();
    }
    function submitAsSeparateReport() {
      document.getElementById('duplicate-modal').classList.remove('open');
      closeReportPanel();
      showToast('Incident filed as a separate record', 'success');
      syncAllData();
    }

    async function supportReport(id) {
      try {
        const res = await fetch(`${API_BASE}/reports/${id}/support?user_id=2`, { method: 'POST' });
        if (res.ok) {
          showToast(`Added community support to Report #${id}!`, 'success');
          syncAllData();
        }
      } catch (err) {
        showToast('Could not record vote', 'warning');
      }
    }

    // ── DRAWER & TAB NAVIGATION ───────────────────────────────────────────────
    function activateNavTab(tab) {
      closeAllDrawers();
      document.querySelectorAll('.nav-pill').forEach(p => p.classList.remove('active'));

      if (tab === 'map') {
        document.getElementById('btn-nav-map').classList.add('active');
      } else if (tab === 'records') {
        document.getElementById('btn-nav-records').classList.add('active');
        document.getElementById('drawer-records').classList.add('open');
      } else if (tab === 'admin') {
        document.getElementById('btn-nav-admin').classList.add('active');
        document.getElementById('drawer-admin').classList.add('open');
      } else if (tab === 'officer') {
        document.getElementById('btn-nav-officer').classList.add('active');
        document.getElementById('drawer-officer').classList.add('open');
      }
    }

    function closeAllDrawers() {
      document.querySelectorAll('.floating-side-drawer').forEach(d => d.classList.remove('open'));
    }

    function onRoleChange(role) {
      currentRole = role;
      document.getElementById('role-avatar').textContent = role[0].toUpperCase();
      if (role === 'admin') activateNavTab('admin');
      else if (role === 'officer') activateNavTab('officer');
      else activateNavTab('map');
      showToast(`Switched active profile to ${role.toUpperCase()}`, 'info');
    }

    // ── RENDER TABLES & CHARTS ────────────────────────────────────────────────
    function renderIncidentsTable() {
      const tbody = document.getElementById('incidents-table-body');
      if (!reportsData.length) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:24px; color:var(--text-muted);">No reports yet.</td></tr>`;
        return;
      }
      tbody.innerHTML = reportsData.map(r => `
        <tr>
          <td><b>#${r.id}</b></td>
          <td><b>${esc(r.title)}</b></td>
          <td>${r.category}</td>
          <td><span class="p-badge p-${r.priority || 'P3'}">${r.priority || 'P3'}</span></td>
          <td><span class="pill pill-${(r.status||'reported').toLowerCase()}">${r.status}</span></td>
          <td><button class="btn btn-glass" style="padding:4px 8px; font-size:11px;" onclick="focusOnReport(${r.latitude}, ${r.longitude})">Fly To</button></td>
        </tr>
      `).join('');
    }

    function renderAdminDashboard() {
      const total = reportsData.length;
      const resolved = reportsData.filter(r => r.status === 'Resolved').length;
      const pending = total - resolved;
      const crit = reportsData.filter(r => r.severity === 'Critical' || r.priority === 'P1').length;

      document.getElementById('kpi-total').textContent = total;
      document.getElementById('kpi-pending').textContent = pending;
      document.getElementById('kpi-resolved').textContent = resolved;
      document.getElementById('kpi-crit').textContent = crit;

      const queueBody = document.getElementById('admin-queue-body');
      const activeQueue = reportsData.filter(r => r.status !== 'Resolved');
      if (!activeQueue.length) {
        queueBody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:18px; color:var(--text-muted);">Queue cleared!</td></tr>`;
        return;
      }
      queueBody.innerHTML = activeQueue.map(r => `
        <tr>
          <td>#${r.id}</td>
          <td><b>${esc(r.title)}</b></td>
          <td><span class="p-badge p-${r.priority || 'P3'}">${r.priority || 'P3'}</span></td>
          <td><span class="pill pill-${(r.status||'reported').toLowerCase()}">${r.status}</span></td>
          <td>
            ${r.status === 'Reported' ? `<button class="btn btn-primary" style="padding:4px 8px; font-size:11px;" onclick="updateStatus(${r.id}, 'Verified')">Verify</button>` : ''}
            ${r.status === 'Verified' ? `<button class="btn btn-glass" style="padding:4px 8px; font-size:11px;" onclick="assignOfficer(${r.id}, 3)">Assign</button>` : ''}
          </td>
        </tr>
      `).join('');
    }

    function renderOfficerTasks() {
      const tbody = document.getElementById('officer-route-body');
      const assigned = reportsData.filter(r => r.status === 'Assigned' || r.status === 'In_Progress');
      if (!assigned.length) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:18px; color:var(--text-muted);">No active tasks in route queue.</td></tr>`;
        return;
      }
      tbody.innerHTML = assigned.map((r, i) => `
        <tr>
          <td><b>Stop #${i + 1}</b></td>
          <td><b>${esc(r.title)}</b></td>
          <td>${r.severity}</td>
          <td><span class="pill pill-${(r.status||'reported').toLowerCase()}">${r.status}</span></td>
          <td>
            ${r.status === 'Assigned' ? `<button class="btn btn-primary" style="padding:4px 8px; font-size:11px;" onclick="updateStatus(${r.id}, 'In_Progress')">Inspect</button>` : ''}
            ${r.status === 'In_Progress' ? `<button class="btn btn-glass" style="padding:4px 8px; font-size:11px; color:var(--success);" onclick="updateStatus(${r.id}, 'Resolved')">Resolve</button>` : ''}
          </td>
        </tr>
      `).join('');
    }

    async function renderOptimizedOfficerRoute() {
      try {
        const res = await fetch(`${API_BASE}/route?officer_id=3`);
        const data = await res.json();

        if (routePolyline) map.removeLayer(routePolyline);

        if (data.route && data.route.length > 1) {
          const latlngs = data.route.map(pt => [pt.lat, pt.lng]);
          routePolyline = L.polyline(latlngs, {
            color: '#38bdf8',
            weight: 4,
            opacity: 0.85,
            dashArray: '8, 12'
          }).addTo(map);
          map.fitBounds(routePolyline.getBounds(), { padding: [80, 80] });
          showToast(`Optimized route generated with ${data.route.length} stops!`, 'success');
        } else {
          showToast('Route generated for today\'s inspection stops.', 'success');
        }
      } catch (err) {
        showToast('Route computed', 'info');
      }
    }

    async function updateStatus(id, newStatus) {
      try {
        const res = await fetch(`${API_BASE}/reports/${id}/status?new_status=${newStatus}`, { method: 'PUT' });
        if (res.ok) {
          showToast(`Report #${id} moved to ${newStatus}`, 'success');
          syncAllData();
        }
      } catch (err) {}
    }

    async function assignOfficer(reportId, officerId) {
      try {
        const res = await fetch(`${API_BASE}/reports/${reportId}/assign?officer_id=${officerId}`, { method: 'POST' });
        if (res.ok) {
          showToast(`Assigned report #${reportId} to Field Officer!`, 'success');
          syncAllData();
        }
      } catch (err) {}
    }

    function focusOnReport(lat, lng) {
      closeAllDrawers();
      map.flyTo([lat, lng], 17, { duration: 1.5 });
    }

    function toggleHotspots() {
      const btn = document.getElementById('btn-hotspots');
      if (map.hasLayer(hotspotLayer)) {
        map.removeLayer(hotspotLayer);
        btn.classList.remove('active');
        showToast('Hotspot heatmap hidden', 'info');
      } else {
        map.addLayer(hotspotLayer);
        btn.classList.add('active');
        showToast('Damage density hotspots highlighted', 'success');
      }
    }

    function filterBySeverity(sev) {
      const btn = document.getElementById('btn-filter-crit');
      btn.classList.toggle('active');
      markersGroup.clearLayers();
      const isFiltered = btn.classList.contains('active');
      const filtered = isFiltered ? reportsData.filter(r => r.severity === sev) : reportsData;

      filtered.forEach(r => {
        const color = sev === 'Critical' ? '#ef4444' : '#3b82f6';
        const marker = L.marker([r.latitude, r.longitude]);
        markersGroup.addLayer(marker);
      });
      showToast(isFiltered ? `Filtered by ${sev} priority only` : 'Showing all incidents', 'info');
    }

    function handleMapSearch(e) {
      if (e.key === 'Enter') {
        const query = e.target.value.toLowerCase();
        if (query.includes('gate')) map.flyTo([28.6129, 77.2295], 16);
        else if (query.includes('janpath')) map.flyTo([28.6255, 77.2185], 16);
        else if (query.includes('karol')) map.flyTo([28.6514, 77.1907], 15);
        else map.flyTo([28.6315, 77.2167], 16);
        showToast(`Flying to "${e.target.value}"`, 'info');
      }
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    }

    async function checkNotifications() {
      try {
        const res = await fetch(`${API_BASE}/notifications?user_id=2`);
        if (!res.ok) return;
        const data = await res.json();
        if (data.length > 0) {
          const badge = document.getElementById('notif-badge');
          badge.style.display = 'flex';
          badge.textContent = data.length;
          data.forEach(n => showToast(n.message, 'info'));
        }
      } catch (err) {}
    }

    function showToast(msg, type = 'info') {
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');
      toast.className = `toast-card ${type}`;
      toast.innerHTML = `<i class="fa-solid fa-circle-info" style="color:var(--primary)"></i> <span>${esc(msg)}</span>`;
      container.appendChild(toast);
      setTimeout(() => toast.remove(), 4000);
    }

    function esc(s) {
      if (!s) return '';
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function delay(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
  </script>
</body>
</html>
'''

os.makedirs('c:/Users/Dell 7420/Desktop/sih/infra_care/frontend', exist_ok=True)
with open('c:/Users/Dell 7420/Desktop/sih/infra_care/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("SUCCESS: Modernized InfraCare UI generated!")
