# -*- coding: utf-8 -*-
"""
Script generador de index.html para Mordheim War Room
Implementa todas las especificaciones de David:
0. Pantalla de Login por PIN para David (1348), Sergio (6995), Javi (7788) y Espectador
1. El Heraldo con portadas xilográficas y selector de ediciones (02 activa por defecto)
2. Misiones con historial por pestañas (Ronda 01 y Ronda 02 activa por defecto con 90x90 vs 120x120)
3. Cartografía Táctica con el nuevo mapa canónico de Mordheim y marcadores tácticos translúcidos
4. Partes de Guerra (AARs)
5. El Oráculo del Metajuego (Reglas OPR v3.6.0, ArmyForge, Escenografía 3D 3MF y Buzón de Sugerencias a Supabase)
6. Contacto con el Heraldo (Roleplay & Lore interactivo con NPCs de Mordheim: Gunter, Lothar, Steinhardt, Loky, Cronista)
7. Panel GM para David con configuración segura de API Key de Gemini en Supabase y visor de sugerencias
"""

html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MORDHEIM: WAR ROOM — Gaceta Táctica &amp; Cuartel General de Campaña</title>

  <!-- Google Fonts de Imprenta Antigua y Gótica -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=IM+Fell+English:ital@0;1&family=Pirata+One&family=MedievalSharp&family=Metamorphous&display=swap" rel="stylesheet">

  <!-- FontAwesome 6 (Iconografía) -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

  <!-- Supabase JS Client para Nube 24/7 -->
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

  <style>
    :root {
      --bg-wood-dark: #120e0a;
      --bg-parchment-sheet: #f6eedb;
      --bg-parchment-dim: #ebdcb9;
      --bg-parchment-aged: #dfcb9f;
      --bg-parchment-light: #fbf3df;
      --line-sepia: #8b7355;
      --line-dark: #3a2e22;
      --ink-black: #17130e;
      --ink-dark: #29221b;
      --ink-muted: #5e5245;

      /* Facciones */
      --faction-david: #7a1515;
      --faction-david-bg: rgba(122, 21, 21, 0.12);
      --faction-sergio: #1b4d24;
      --faction-sergio-bg: rgba(27, 77, 36, 0.12);
      --faction-javi: #8a4f08;
      --faction-javi-bg: rgba(138, 79, 8, 0.12);
      --faction-neutral: #575249;
      --faction-neutral-bg: rgba(87, 82, 73, 0.12);

      --font-gothic: 'Pirata One', 'MedievalSharp', fantasy, serif;
      --font-title: 'Cinzel', 'Times New Roman', serif;
      --font-body: 'IM Fell English', Georgia, serif;
      --font-press-title: 'Metamorphous', 'Cinzel', serif;
      --font-press-body: 'IM Fell English', Georgia, serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg-wood-dark);
      background-image:
        radial-gradient(circle at 50% 10%, rgba(246, 238, 219, 0.08) 0%, transparent 60%),
        repeating-linear-gradient(0deg, rgba(0,0,0,0.18) 0px, rgba(0,0,0,0.18) 1px, transparent 1px, transparent 3px);
      color: var(--ink-dark);
      font-family: var(--font-body);
      font-size: 15px;
      line-height: 1.5;
      min-height: 100vh;
      padding: 0.6rem 0.6rem 2.5rem 0.6rem;
    }

    /* CONTENEDOR CENTRAL DE LA GACETA */
    .gazette-wrapper {
      max-width: 1220px;
      margin: 0 auto;
      background: var(--bg-parchment-sheet);
      background-image:
        radial-gradient(#d8c49a 0.8px, transparent 0.8px),
        linear-gradient(to bottom, rgba(255,255,255,0.2), rgba(0,0,0,0.04));
      background-size: 20px 20px, 100% 100%;
      border: 4px solid var(--ink-black);
      box-shadow:
        0 0 0 2px var(--bg-parchment-sheet),
        0 0 0 5px var(--ink-black),
        0 15px 35px rgba(0, 0, 0, 0.7);
      position: relative;
    }

    /* CABECERA DE IMPRENTA GÓTICA */
    .gazette-header {
      padding: 1rem 1.4rem 0.8rem 1.4rem;
      border-bottom: 3px double var(--ink-black);
      background: var(--bg-parchment-dim);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }

    .header-branding { display: flex; align-items: center; gap: 1rem; }
    .header-logo-icon {
      font-size: 2.2rem;
      color: var(--faction-david);
      filter: drop-shadow(2px 2px 0 rgba(0,0,0,0.3));
    }
    .header-title-main {
      font-family: var(--font-gothic);
      font-size: 2.2rem;
      line-height: 1.05;
      color: var(--ink-black);
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }
    .header-sub-main {
      font-family: var(--font-title);
      font-size: 0.75rem;
      letter-spacing: 0.12em;
      color: var(--ink-muted);
      text-transform: uppercase;
      font-weight: 700;
      margin-top: 2px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 0.8rem;
      flex-wrap: wrap;
    }

    .identity-chip {
      background: var(--bg-parchment-sheet);
      border: 1.5px solid var(--ink-black);
      padding: 0.35rem 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      box-shadow: 2px 2px 0 var(--ink-black);
      font-family: var(--font-title);
      font-size: 0.8rem;
      font-weight: 700;
    }

    .btn-action {
      background: var(--bg-parchment-sheet);
      border: 1.5px solid var(--ink-black);
      color: var(--ink-black);
      font-family: var(--font-title);
      font-weight: 700;
      font-size: 0.76rem;
      padding: 0.4rem 0.8rem;
      cursor: pointer;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      box-shadow: 2px 2px 0 var(--ink-black);
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      text-decoration: none;
      transition: all 0.12s ease;
    }
    .btn-action:hover {
      background: #ffffff;
      transform: translate(-1px, -1px);
      box-shadow: 3px 3px 0 var(--ink-black);
    }
    .btn-action:active {
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0 var(--ink-black);
    }
    .btn-action.btn-danger {
      background: #ebd2d2;
      color: var(--faction-david);
      border-color: var(--faction-david);
    }

    /* TIRA DE FOLIO / METADATOS DE IMPRENTA */
    .gazette-folio-strip {
      border-bottom: 2px solid var(--ink-black);
      background: #e4d3a9;
      display: flex;
      justify-content: space-between;
      padding: 0.3rem 1.4rem;
      font-family: var(--font-title);
      font-size: 0.7rem;
      font-weight: 800;
      color: var(--ink-black);
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    /* MARCADOR DE CAMPAÑA SUPERIOR */
    .scoreboard-strip {
      border-bottom: 2px solid var(--ink-black);
      background: #ecdcba;
      padding: 0.6rem 1.4rem;
    }
    .scoreboard-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 0.8rem;
    }
    .commander-card {
      background: var(--bg-parchment-sheet);
      border: 1.5px solid var(--ink-black);
      padding: 0.6rem 0.8rem;
      box-shadow: 2px 2px 0 var(--ink-black);
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }
    .commander-card.david { border-left: 5px solid var(--faction-david); }
    .commander-card.sergio { border-left: 5px solid var(--faction-sergio); }
    .commander-card.javi { border-left: 5px solid var(--faction-javi); }

    .cmd-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .cmd-identity {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .cmd-avatar { font-size: 1.3rem; }
    .cmd-name { font-size: 0.92rem; font-weight: 800; font-family: var(--font-title); color: var(--ink-black); }
    .cmd-faction { font-size: 0.72rem; color: var(--ink-muted); font-style: italic; }
    .cmd-stats {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      border: 1px solid var(--line-sepia);
      background: #faf4e6;
      padding: 0.25rem 0.4rem;
      text-align: center;
    }
    .stat-val { font-size: 1.15rem; font-weight: 800; font-family: var(--font-title); }
    .stat-lbl { font-size: 0.62rem; color: var(--ink-muted); text-transform: uppercase; font-family: var(--font-title); }

    /* NAVEGACIÓN POR PESTAÑAS (FOLIO TABS) */
    .tabs-nav {
      display: flex;
      background: #decba2;
      border-bottom: 2px solid var(--ink-black);
      overflow-x: auto;
      scrollbar-width: none;
      padding: 0.35rem 0.6rem 0 0.6rem;
      gap: 0.3rem;
    }
    .tabs-nav::-webkit-scrollbar { display: none; }

    .tab-btn {
      background: #ebd9b5;
      border: 1.5px solid var(--ink-black);
      border-bottom: none;
      color: var(--ink-dark);
      font-family: var(--font-title);
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.04em;
      padding: 0.55rem 0.95rem;
      cursor: pointer;
      text-transform: uppercase;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      white-space: nowrap;
      transition: all 0.12s ease;
      position: relative;
      top: 1px;
    }
    .tab-btn:hover { background: #fbf5e6; }
    .tab-btn.active {
      background: var(--bg-parchment-sheet);
      border-bottom: 2px solid var(--bg-parchment-sheet);
      color: var(--ink-black);
      box-shadow: 0 -2px 0 var(--ink-black);
      font-weight: 900;
    }
    .tab-btn.gm-only {
      color: var(--faction-david);
      border-color: var(--faction-david);
      background: #fae8e8;
    }
    .tab-btn.gm-only.active {
      background: var(--bg-parchment-sheet);
      border-color: var(--ink-black);
    }

    /* CONTENIDO DE LAS PESTAÑAS */
    .tab-pane {
      display: none;
      padding: 1.4rem;
      animation: fadeIn 0.15s ease-in-out;
    }
    .tab-pane.active { display: block; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    /* PESTAÑA 0: LOGIN VIEW (GATEWAY) */
    .login-container {
      max-width: 680px;
      margin: 1.5rem auto;
      border: 3px double var(--ink-black);
      background: #faf4e6;
      padding: 1.8rem;
      box-shadow: 4px 4px 0 rgba(0,0,0,0.25);
      text-align: center;
    }
    .login-crest {
      font-size: 3rem;
      color: var(--faction-david);
      margin-bottom: 0.5rem;
    }
    .login-title {
      font-family: var(--font-gothic);
      font-size: 2.2rem;
      color: var(--ink-black);
      line-height: 1.1;
      margin-bottom: 0.4rem;
    }
    .login-subtitle {
      font-family: var(--font-title);
      font-size: 0.8rem;
      color: var(--ink-muted);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 1.5rem;
    }

    .login-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
      margin-bottom: 1.5rem;
      text-align: left;
    }
    @media (max-width: 600px) { .login-grid { grid-template-columns: 1fr; } }

    .login-user-card {
      border: 2px solid var(--ink-black);
      background: var(--bg-parchment-sheet);
      padding: 0.85rem;
      cursor: pointer;
      box-shadow: 2px 2px 0 var(--ink-black);
      display: flex;
      align-items: center;
      gap: 0.8rem;
      transition: all 0.12s ease;
    }
    .login-user-card:hover {
      background: #ffffff;
      transform: translate(-1px, -1px);
      box-shadow: 3px 3px 0 var(--ink-black);
    }
    .login-user-card.selected {
      border-color: var(--faction-david);
      background: #fbf2f2;
      box-shadow: 3px 3px 0 var(--faction-david);
    }
    .login-avatar { font-size: 1.6rem; }
    .login-card-title { font-family: var(--font-title); font-size: 0.92rem; font-weight: 800; color: var(--ink-black); }
    .login-card-desc { font-size: 0.72rem; color: var(--ink-muted); font-style: italic; }

    .login-pin-box {
      border: 2px dashed var(--ink-black);
      background: #fdfaf3;
      padding: 1.2rem;
      max-width: 360px;
      margin: 0 auto;
      display: none;
    }
    .login-pin-input {
      width: 140px;
      font-family: var(--font-title);
      font-size: 1.3rem;
      letter-spacing: 0.3em;
      text-align: center;
      padding: 0.4rem;
      border: 2px solid var(--ink-black);
      background: #ffffff;
      margin: 0.6rem 0;
    }

    /* PESTAÑA 1: EL HERALDO */
    .herald-nav {
      display: flex;
      gap: 0.4rem;
      margin-bottom: 1rem;
      flex-wrap: wrap;
    }
    .border-woodcut-double {
      border: 3px double #241d17;
      background: #f4ecdc;
      padding: 1.2rem;
      box-shadow: inset 0 0 10px rgba(0,0,0,0.06);
    }
    .woodcut-crop {
      width: 100%;
      height: auto;
      max-height: 440px;
      object-fit: cover;
      filter: contrast(1.15) brightness(0.96) sepia(0.28);
      mix-blend-mode: multiply;
      display: block;
    }
    .drop-cap {
      float: left;
      font-family: var(--font-gothic);
      font-size: 3.4rem;
      line-height: 0.8;
      padding-right: 8px;
      padding-top: 4px;
      color: #611515;
    }

    /* PESTAÑA 2: MISIONES */
    .mission-nav-bar {
      display: flex;
      gap: 0.4rem;
      margin-bottom: 1.2rem;
      border-bottom: 2px solid var(--ink-black);
      padding-bottom: 0.4rem;
    }
    .mission-layout {
      display: grid;
      grid-template-columns: 1.25fr 0.75fr;
      gap: 1.2rem;
    }
    @media (max-width: 860px) { .mission-layout { grid-template-columns: 1fr; } }

    .panel-box {
      border: 3px double var(--ink-black);
      background: var(--bg-parchment-sheet);
      padding: 1.2rem;
      box-shadow: 3px 3px 0 rgba(0,0,0,0.12);
    }
    .panel-title-strip {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--ink-black);
      padding-bottom: 0.5rem;
      margin-bottom: 0.9rem;
    }
    .spec-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 0.6rem;
      margin-bottom: 1rem;
    }
    .spec-cell {
      border: 1px solid var(--ink-black);
      border-left: 4px solid var(--ink-black);
      background: #faf4e6;
      padding: 0.5rem;
    }
    .spec-cell-lbl { font-size: 0.65rem; color: var(--ink-muted); text-transform: uppercase; font-family: var(--font-title); font-weight: 800; }
    .spec-cell-val { font-size: 0.95rem; font-weight: 800; color: var(--ink-black); font-family: var(--font-title); }

    .confidential-seal {
      background: #faf2f2;
      border: 2px solid var(--faction-david);
      padding: 1.2rem;
      position: relative;
      overflow: hidden;
      box-shadow: 3px 3px 0 var(--faction-david);
    }
    .confidential-seal::before {
      content: "CONFIDENCIAL";
      position: absolute;
      right: -28px;
      top: 16px;
      background: var(--faction-david);
      color: #fff;
      font-size: 0.62rem;
      font-weight: 900;
      font-family: var(--font-title);
      padding: 0.2rem 2.2rem;
      transform: rotate(45deg);
      border: 1px dashed #fff;
      letter-spacing: 0.15em;
    }

    /* PESTAÑA 3: CARTOGRAFÍA TÁCTICA */
    .map-grid-layout {
      display: grid;
      grid-template-columns: 1.3fr 0.7fr;
      gap: 1.2rem;
      align-items: start;
    }
    @media (max-width: 950px) { .map-grid-layout { grid-template-columns: 1fr; } }

    .tactical-map-viewport {
      position: relative;
      border: 3px double var(--ink-black);
      background: #ede1c7;
      box-shadow: 4px 4px 0 rgba(0,0,0,0.2);
      overflow: hidden;
    }
    .tactical-map-img {
      width: 100%;
      height: auto;
      display: block;
      filter: contrast(1.08) brightness(0.98);
    }
    .tactical-map-overlay {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
    }

    /* Marcador elegante de mapa */
    .map-pin {
      cursor: pointer;
      transition: transform 0.15s ease, filter 0.15s ease;
    }
    .map-pin:hover {
      transform: scale(1.18);
      filter: drop-shadow(0 0 6px rgba(0,0,0,0.6));
    }
    .map-pin.active .pin-ring {
      stroke: #ffffff;
      stroke-width: 2.5;
      filter: drop-shadow(0 0 8px #ffd700);
    }

    /* PESTAÑA 5: EL ORÁCULO & BUZÓN */
    .oracle-layout {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.2rem;
    }
    @media (max-width: 860px) { .oracle-layout { grid-template-columns: 1fr; } }

    .chat-box-feed {
      height: 380px;
      overflow-y: auto;
      border: 2px solid var(--ink-black);
      background: #fdfaf3;
      padding: 0.8rem;
      display: flex;
      flex-direction: column;
      gap: 0.8rem;
      margin-bottom: 0.8rem;
    }
    .chat-bubble {
      padding: 0.75rem 0.9rem;
      border: 1px solid var(--ink-black);
      font-size: 0.88rem;
      line-height: 1.45;
      max-width: 88%;
      box-shadow: 2px 2px 0 rgba(0,0,0,0.1);
    }
    .chat-bubble.bot {
      align-self: flex-start;
      background: var(--bg-parchment-sheet);
      border-left: 4px solid var(--faction-david);
    }
    .chat-bubble.user {
      align-self: flex-end;
      background: #e8edd8;
      border-right: 4px solid var(--faction-sergio);
    }
    .chat-bubble.npc {
      align-self: flex-start;
      background: #fbf5e6;
      border-left: 4px solid #8a4f08;
    }

    .form-control {
      width: 100%;
      border: 1.5px solid var(--ink-black);
      background: #ffffff;
      padding: 0.55rem 0.75rem;
      font-family: var(--font-body);
      font-size: 0.9rem;
      color: var(--ink-black);
      box-shadow: inset 1px 1px 3px rgba(0,0,0,0.1);
    }
    textarea.form-control { resize: vertical; min-height: 80px; }

    /* PESTAÑA 6: CONTACTO CON EL HERALDO (NPCS) */
    .npc-selector-bar {
      display: flex;
      gap: 0.5rem;
      overflow-x: auto;
      padding-bottom: 0.4rem;
      margin-bottom: 1rem;
      scrollbar-width: none;
    }
    .npc-card-btn {
      border: 2px solid var(--ink-black);
      background: var(--bg-parchment-dim);
      padding: 0.5rem 0.8rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-family: var(--font-title);
      font-size: 0.78rem;
      font-weight: 800;
      white-space: nowrap;
      transition: all 0.12s ease;
      box-shadow: 2px 2px 0 var(--ink-black);
    }
    .npc-card-btn:hover { background: #fff; }
    .npc-card-btn.active {
      background: var(--bg-parchment-sheet);
      border-color: var(--faction-david);
      box-shadow: 3px 3px 0 var(--faction-david);
      color: var(--faction-david);
    }

    /* PIE DE PÁGINA */
    .gazette-footer {
      border-top: 3px double var(--ink-black);
      background: var(--bg-parchment-dim);
      padding: 0.8rem 1.4rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.8rem;
      font-size: 0.72rem;
      font-family: var(--font-title);
      font-weight: 700;
      color: var(--ink-muted);
    }
    .sync-status { display: flex; align-items: center; gap: 0.4rem; font-weight: 800; }
    .sync-dot { width: 8px; height: 8px; border-radius: 50%; background: #2b8a3e; box-shadow: 0 0 5px #2b8a3e; }
    .sync-dot.offline { background: #d97706; box-shadow: none; }
  </style>
</head>
<body>

  <div class="gazette-wrapper">

    <!-- CABECERA PRINCIPAL -->
    <header class="gazette-header">
      <div class="header-branding">
        <i class="fa-solid fa-skull-crossbones header-logo-icon"></i>
        <div>
          <h1 class="header-title-main">Mordheim: War Room</h1>
          <div class="header-sub-main">Cuartel General &amp; Registro Táctico Oficial • Age of Fantasy: Skirmish v3.6.0</div>
        </div>
      </div>
      <div class="header-actions">
        <!-- Chip de usuario identificado -->
        <div class="identity-chip" id="userHeaderChip">
          <span id="userHeaderAvatar">👁️</span>
          <span id="userHeaderName">Identifícate</span>
        </div>
        <button class="btn-action" id="btnLogout" onclick="app.logout()">
          <i class="fa-solid fa-arrow-right-from-bracket"></i> Salir / Cambiar
        </button>
      </div>
    </header>

    <!-- TIRA DE FOLIO / METADATOS -->
    <div class="gazette-folio-strip">
      <span><i class="fa-solid fa-landmark"></i> ARCHIVOS DEL TRIBUNAL DE GUERRA</span>
      <span>AÑO DE LAS SOMBRAS 1599 • IMPRENTA DE LA CIUDAD CONDENADA</span>
      <span id="headerRoundTag">RONDA 02 EN CURSO</span>
    </div>

    <!-- MARCADOR DE CAMPAÑA (TRES FACCIONES) -->
    <section class="scoreboard-strip" id="campaignScoreboard">
      <div class="scoreboard-grid" id="scoreboardCardsGrid">
        <!-- Inyectado por JS -->
      </div>
    </section>

    <!-- BARRA DE PESTAÑAS (ORDEN DE DAVID: 1 Heraldo, 2 Misiones, 3 Mapa, 4 AAR, 5 Oráculo, 6 Contacto, 7 GM) -->
    <nav class="tabs-nav" id="mainTabsNav">
      <button class="tab-btn active" data-tab="tab-gazette">
        <i class="fa-solid fa-newspaper"></i> 1. El Heraldo
      </button>
      <button class="tab-btn" data-tab="tab-mission">
        <i class="fa-solid fa-shield-halved"></i> 2. Misiones
      </button>
      <button class="tab-btn" data-tab="tab-map">
        <i class="fa-solid fa-map-location-dot"></i> 3. Cartografía Táctica
      </button>
      <button class="tab-btn" data-tab="tab-aar">
        <i class="fa-solid fa-scroll"></i> 4. Partes de Guerra
      </button>
      <button class="tab-btn" data-tab="tab-oracle">
        <i class="fa-solid fa-balance-scale"></i> 5. El Oráculo
      </button>
      <button class="tab-btn" data-tab="tab-roleplay">
        <i class="fa-solid fa-comments"></i> 6. Contacto con el Heraldo
      </button>
      <button class="tab-btn gm-only" data-tab="tab-gm" id="tabGmBtn" style="display: none;">
        <i class="fa-solid fa-crown"></i> 7. Panel GM
      </button>
    </nav>

    <main class="war-main">

      <!-- ======================================================== -->
      <!-- PESTAÑA 0: LOGIN DE ENTRADA (GUARDIA DE MORDHEIM)       -->
      <!-- ======================================================== -->
      <section class="tab-pane" id="tab-login">
        <div class="login-container">
          <div class="login-crest"><i class="fa-solid fa-shield-halved"></i></div>
          <h2 class="login-title">Puesto de Control de la Guardia</h2>
          <p class="login-subtitle">Selecciona tu credencial e introduce tu clave de acceso secreta</p>

          <div class="login-grid">
            <!-- David -->
            <div class="login-user-card" onclick="app.selectLoginUser('david')">
              <span class="login-avatar">🧛</span>
              <div>
                <div class="login-card-title">David</div>
                <div class="login-card-desc">Lord Carmesí &amp; Árbitro GM</div>
              </div>
            </div>
            <!-- Sergio -->
            <div class="login-user-card" onclick="app.selectLoginUser('sergio')">
              <span class="login-avatar">🐀</span>
              <div>
                <div class="login-card-title">Sergio</div>
                <div class="login-card-desc">Señor del Clan Scutrix</div>
              </div>
            </div>
            <!-- Javi -->
            <div class="login-user-card" onclick="app.selectLoginUser('javi')">
              <span class="login-avatar">⚒️</span>
              <div>
                <div class="login-card-title">Javi</div>
                <div class="login-card-desc">Patriarca Hijos del Yunque</div>
              </div>
            </div>
            <!-- Espectador -->
            <div class="login-user-card" onclick="app.selectLoginUser('spectator')">
              <span class="login-avatar">👁️</span>
              <div>
                <div class="login-card-title">Espectador Neutral</div>
                <div class="login-card-desc">Acceso libre (Sin secretos)</div>
              </div>
            </div>
          </div>

          <!-- Cuadro de PIN -->
          <div class="login-pin-box" id="loginPinBox">
            <div style="font-family: var(--font-title); font-weight: 800; font-size: 0.85rem;" id="loginPinPrompt">Introduce tu PIN</div>
            <input type="password" id="loginPinInput" class="login-pin-input" maxlength="4" placeholder="****" onkeyup="if(event.key==='Enter') app.submitPin()"/>
            <div>
              <button class="btn-action" onclick="app.submitPin()" style="padding: 0.5rem 1.4rem;">
                <i class="fa-solid fa-key"></i> Entrar a la Sala
              </button>
            </div>
            <div id="loginPinError" style="font-size: 0.76rem; color: var(--faction-david); font-weight: 800; margin-top: 0.5rem; display: none;">
              PIN incorrecto. Consulta con el Árbitro.
            </div>
          </div>
        </div>
      </section>

      <!-- ======================================================== -->
      <!-- PESTAÑA 1: EL HERALDO DE MORDHEIM (FOLIO 1)             -->
      <!-- ======================================================== -->
      <section class="tab-pane active" id="tab-gazette">
        <!-- Selector de Edición -->
        <div class="herald-nav">
          <button class="btn-action" id="btnGazette0" onclick="app.showGazette(0)">
            <i class="fa-solid fa-meteor"></i> Edición 00 (Fundacional)
          </button>
          <button class="btn-action" id="btnGazette1" onclick="app.showGazette(1)">
            <i class="fa-solid fa-shield"></i> Edición 01 (Apertura)
          </button>
          <button class="btn-action active" id="btnGazette2" onclick="app.showGazette(2)">
            <i class="fa-solid fa-skull"></i> Edición 02 (Última: ¡La Fuga de Loky!)
          </button>
        </div>

        <article class="border-woodcut-double">
          <!-- Cabecera del Diario -->
          <div style="text-align: center; border-bottom: 2px solid #28211b; padding-bottom: 8px; margin-bottom: 12px;">
            <div style="font-family: var(--font-title); font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; color: #5a4b3d;" id="gazetteIssueMeta">
              Número 2 (Extraordinaria) • Tras la Batalla en el Bastión Central
            </div>
            <h2 id="gazetteLeadTitle" style="font-family: var(--font-gothic); font-size: 2.5rem; line-height: 1.05; color: #1a1613; margin: 4px 0;">
              ¡LA MASACRE Y LA FUGA DE LOKY!
            </h2>
            <div id="gazetteSublead" style="font-family: var(--font-title); font-size: 0.95rem; font-weight: 700; color: #6a1a1a; letter-spacing: 0.08em; text-transform: uppercase;">
              COBARDÍA HISTÓRICA EN LA ENCRUCIJADA
            </div>
          </div>

          <!-- Cuadrícula: Crónica + Xilografía -->
          <div style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 16px; align-items: start;">
            <!-- Crónica Izquierda -->
            <div id="gazetteLeftCol" style="font-size: 0.95rem; text-align: justify; color: #1d1814;">
              <!-- Inyectado por JS -->
            </div>
            <!-- Xilografía Derecha -->
            <div>
              <div style="border: 2px solid #221c17; background: var(--bg-parchment-light); padding: 4px; box-shadow: 3px 3px 0 rgba(0,0,0,0.2);">
                <img id="gazetteMainImg" src="./assets/portada_edicion_02.jpg" alt="Grabado oficial" class="woodcut-crop" />
                <p id="gazetteImgCaption" style="font-size: 0.78rem; text-align: center; font-style: italic; margin-top: 6px; font-weight: 700; color: #2d241c;">
                  Xilografía Clandestina: La cobarde fuga de Loky en su carromato de mulas tras la refriega en la encrucijada.
                </p>
              </div>
              <div style="text-align: center; margin-top: 10px;">
                <a id="gazettePdfLink" href="./assets/El_Heraldo_de_mordheim_Edicion_02.pdf" target="_blank" class="btn-action">
                  <i class="fa-solid fa-file-pdf"></i> Abrir Edición Completa en PDF
                </a>
              </div>
            </div>
          </div>
        </article>
      </section>

      <!-- ======================================================== -->
      <!-- PESTAÑA 2: MISIONES & ÓRDENES SECRETAS (FOLIO 2)        -->
      <!-- ======================================================== -->
      <section class="tab-pane" id="tab-mission">
        <!-- Selector de Misiones -->
        <div class="mission-nav-bar">
          <button class="btn-action" id="btnMission1" onclick="app.showMission(1)">
            <i class="fa-solid fa-flag-checkered"></i> Ronda 01: El Despertar del Colmillo
          </button>
          <button class="btn-action active" id="btnMission2" onclick="app.showMission(2)">
            <i class="fa-solid fa-meteor"></i> Ronda 02: La Caza de la Piedra Bruja (Activa)
          </button>
        </div>

        <div class="mission-layout">
          <!-- Columna Izquierda: Detalles de la Misión -->
          <div class="panel-box">
            <div class="panel-title-strip">
              <h3 class="panel-title" id="missionTitleDisplay" style="font-family: var(--font-gothic); font-size: 1.6rem;">
                Ronda 02: La Caza de la Piedra Bruja en las Ruinas
              </h3>
              <span class="rank-tag" id="missionStatusBadge" style="background: var(--faction-sergio-bg); color: var(--faction-sergio); border: 1.5px solid var(--faction-sergio); padding: 0.2rem 0.6rem; font-weight: 800; font-family: var(--font-title); font-size: 0.72rem;">
                RONDA EN CURSO
              </span>
            </div>

            <!-- Especificaciones -->
            <div class="spec-grid">
              <div class="spec-cell">
                <div class="spec-cell-lbl">Reglamento</div>
                <div class="spec-cell-val" id="missionRulebook">AoF: Skirmish v3.6.0</div>
              </div>
              <div class="spec-cell">
                <div class="spec-cell-lbl">Puntos de Banda</div>
                <div class="spec-cell-val" id="missionPoints">600 pts (+botín)</div>
              </div>
              <div class="spec-cell">
                <div class="spec-cell-lbl">Límite de Rondas</div>
                <div class="spec-cell-val" id="missionTurns">4 Rondas</div>
              </div>
              <div class="spec-cell">
                <div class="spec-cell-lbl">Mesa de Asedio</div>
                <div class="spec-cell-val" id="missionTableSize">90x90 (David) / 120x120 (Sergio &amp; Javi)</div>
              </div>
            </div>

            <!-- Trasfondo y Objetivos -->
            <div style="margin-bottom: 1rem;">
              <h4 style="font-family: var(--font-title); font-size: 0.88rem; color: var(--ink-black); margin-bottom: 0.4rem; border-bottom: 1px dashed var(--line-sepia); padding-bottom: 0.2rem;">
                <i class="fa-solid fa-scroll"></i> Trasfondo Bélico &amp; Directivas de Escaramuza
              </h4>
              <p id="missionLoreText" style="font-size: 0.92rem; color: var(--ink-dark); margin-bottom: 0.8rem; line-height: 1.5;">
                <!-- Inyectado por JS -->
              </p>
              <h4 style="font-family: var(--font-title); font-size: 0.88rem; color: var(--ink-black); margin-bottom: 0.4rem;">
                <i class="fa-solid fa-bullseye"></i> Objetivos Tácticos:
              </h4>
              <ul id="missionObjectivesList" style="padding-left: 1.4rem; font-size: 0.9rem; line-height: 1.6; color: var(--ink-dark);">
                <!-- Inyectado por JS -->
              </ul>
            </div>

            <div style="display: flex; gap: 0.8rem; flex-wrap: wrap;">
              <a href="./assets/Hoja_Mision_Ronda_01.pdf" target="_blank" class="btn-action">
                <i class="fa-solid fa-file-pdf"></i> Descargar Orden de Batalla en PDF
              </a>
              <a href="./assets/Mapa_Mesa_90x90_Escaramuza.png" target="_blank" class="btn-action">
                <i class="fa-solid fa-map"></i> Plano de Despliegue de Mesa
              </a>
            </div>
          </div>

          <!-- Columna Derecha: Órdenes Secretas (Niebla de Guerra) -->
          <div>
            <div class="confidential-seal">
              <div style="font-family: var(--font-title); font-weight: 800; font-size: 0.82rem; color: var(--faction-david); margin-bottom: 0.4rem;">
                <i class="fa-solid fa-user-secret"></i> DIRECTIVA CLANDESTINA DE FACCIÓN
              </div>
              <div id="fogOfWarSecretBox">
                <!-- Inyectado por JS según el usuario autenticado -->
              </div>
            </div>

            <!-- Tabla de Tamaño de Mesa Acordado -->
            <div style="margin-top: 1rem; border: 2px solid var(--ink-black); background: #faf4e6; padding: 0.8rem; font-size: 0.82rem;">
              <div style="font-family: var(--font-title); font-weight: 800; color: var(--ink-black); margin-bottom: 0.4rem;">
                <i class="fa-solid fa-ruler-combined"></i> Normativa de Mesas de Juego
              </div>
              <p style="margin-bottom: 0.4rem;">
                <strong>Casa de David:</strong> 90 x 90 cm (Pasadizos estrechos, criptas y combate cerrado).
              </p>
              <p>
                <strong>Casa de Sergio / Javi (Loky):</strong> 120 x 120 cm (Grandes plazas, avenidas derruidas y maniobra exterior).
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- ======================================================== -->
      <!-- PESTAÑA 3: CARTOGRAFÍA TÁCTICA (NUEVO MAPA MORDHEIM)    -->
      <!-- ======================================================== -->
      <section class="tab-pane" id="tab-map">
        <div class="map-grid-layout">
          <!-- Visor del Mapa de Mordheim -->
          <div class="tactical-map-viewport">
            <img src="./assets/mapa_mordheim.jpg" alt="Mapa Canónico de Mordheim" class="tactical-map-img" />
            <!-- Capa interactiva SVG ajustada a 1077x794 -->
            <svg class="tactical-map-overlay" viewBox="0 0 1077 794" id="mordheimSvgMap">
              <!-- Nodos interactivos generados por JS -->
            </svg>
          </div>

          <!-- Ficha de Distrito Seleccionado -->
          <div class="panel-box">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--ink-black); padding-bottom: 0.4rem; margin-bottom: 0.6rem;">
              <span id="districtDetailNum" style="font-family: var(--font-title); font-weight: 800; font-size: 0.82rem;">DISTRITO I</span>
              <span class="district-badge" id="districtDetailBadge" style="padding: 0.2rem 0.6rem; font-weight: 800; font-family: var(--font-title); font-size: 0.72rem; border: 1.5px solid var(--ink-black);">Control: Sergio</span>
            </div>

            <h3 id="districtDetailName" style="font-family: var(--font-gothic); font-size: 1.8rem; color: var(--ink-black); margin-bottom: 0.4rem;">La Roca de Sigmar</h3>

            <div style="background: #faf4e6; border: 1.5px dashed var(--ink-black); padding: 0.75rem; margin-bottom: 0.8rem;">
              <div style="font-family: var(--font-title); font-size: 0.75rem; font-weight: 800; color: var(--faction-david); text-transform: uppercase;">
                <i class="fa-solid fa-scroll"></i> Privilegio Táctico:
              </div>
              <div id="districtDetailPerk" style="font-size: 0.92rem; font-style: italic; color: var(--ink-dark); margin-top: 2px;">
                «Vigilancia Sacra: Permite desplegar 1 unidad con Scout a 12 pulgadas del despliegue base.»
              </div>
            </div>

            <p id="districtDetailLore" style="font-size: 0.88rem; color: var(--ink-muted); line-height: 1.45; margin-bottom: 1rem;">
              Monasterio insular en mitad del cauce del río Stir. Soportó la onda expansiva del cometa gracias a la devoción de sus defensoras.
            </p>

            <!-- Controles GM (Solo David) -->
            <div id="districtGmBox" style="display: none; border-top: 2px solid var(--faction-david); padding-top: 0.8rem; background: #faf2f2; padding: 0.6rem;">
              <div style="font-family: var(--font-title); font-size: 0.72rem; font-weight: 800; color: var(--faction-david); margin-bottom: 0.4rem;">
                <i class="fa-solid fa-crown"></i> Arbitraje GM: Asignar Soberanía Territorial
              </div>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem;">
                <button class="btn-action" onclick="app.setDistrictOwner('david')">🧛 David</button>
                <button class="btn-action" onclick="app.setDistrictOwner('sergio')">🐀 Sergio</button>
                <button class="btn-action" onclick="app.setDistrictOwner('javi')">⚒️ Javi</button>
                <button class="btn-action" onclick="app.setDistrictOwner('neutral')">🛡️ Neutral</button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ======================================================== -->
      <!-- PESTAÑA 4: PARTES DE GUERRA (AARs) (FOLIO 4)             -->
      <!-- ======================================================== -->
      <section class="tab-pane" id="tab-aar">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem;">
          <!-- Enviar nuevo Parte -->
          <div class="panel-box">
            <h3 style="font-family: var(--font-gothic); font-size: 1.5rem; margin-bottom: 0.6rem;">
              <i class="fa-solid fa-feather-pointed"></i> Grabar Despacho Inmediato
            </h3>
            <form onsubmit="app.submitAar(event)">
              <div style="margin-bottom: 0.6rem;">
                <label style="font-size: 0.75rem; font-weight: 800; font-family: var(--font-title);">Rival Enfrentado:</label>
                <select id="aarOpponent" class="form-control">
                  <option value="Sergio (Clan Scutrix)">Sergio (Clan Scutrix)</option>
                  <option value="David (Sangre Carmesí)">David (Sangre Carmesí)</option>
                  <option value="Javi (Hijos del Yunque)">Javi (Hijos del Yunque)</option>
                  <option value="Guarnición Neutral">Guarnición Neutral</option>
                </select>
              </div>
              <div style="margin-bottom: 0.6rem;">
                <label style="font-size: 0.75rem; font-weight: 800; font-family: var(--font-title);">Resultado del Choque:</label>
                <select id="aarResult" class="form-control">
                  <option value="Victoria Decisiva (+2 VP)">Victoria Decisiva (+2 VP)</option>
                  <option value="Victoria Pírrica (+1.5 VP)">Victoria Pírrica (+1.5 VP)</option>
                  <option value="Empate Sangriento (+1 VP)">Empate Sangriento (+1 VP)</option>
                  <option value="Derrota Táctica (+0.5 VP)">Derrota Táctica (+0.5 VP)</option>
                  <option value="Masacre Sufrida (0 VP)">Masacre Sufrida (0 VP)</option>
                </select>
              </div>
              <div style="margin-bottom: 0.8rem;">
                <label style="font-size: 0.75rem; font-weight: 800; font-family: var(--font-title);">Crónica de la Refriega:</label>
                <textarea id="aarStory" class="form-control" placeholder="Relata el choque, las bajas y los momentos gloriosos de tu banda..." required></textarea>
              </div>
              <button type="submit" class="btn-action">
                <i class="fa-solid fa-stamp"></i> Sellar Parte y Sincronizar
              </button>
            </form>
          </div>

          <!-- Historial de Partes -->
          <div class="panel-box">
            <h3 style="font-family: var(--font-gothic); font-size: 1.5rem; margin-bottom: 0.6rem;">
              <i class="fa-solid fa-scroll"></i> Despachos Anteriores
            </h3>
            <div id="aarFeedContainer" style="max-height: 440px; overflow-y: auto; display: flex; flex-direction: column; gap: 0.8rem;">
              <!-- Inyectado por JS -->
            </div>
          </div>
        </div>
      </section>

      <!-- ======================================================== -->
      <!-- PESTAÑA 5: EL ORÁCULO DEL METAJUEGO & BUZÓN (FOLIO 5)    -->
      <!-- ======================================================== -->
      <section class="tab-pane" id="tab-oracle">
        <div class="oracle-layout">
          <!-- Columna Izquierda: Asistente de Reglas & Metajuego -->
          <div class="panel-box">
            <h3 style="font-family: var(--font-gothic); font-size: 1.5rem; margin-bottom: 0.4rem;">
              <i class="fa-solid fa-balance-scale"></i> Consultorio de Reglas &amp; Metajuego
            </h3>
            <p style="font-size: 0.82rem; color: var(--ink-muted); margin-bottom: 0.8rem;">
              Pregunta cualquier duda sobre <em>Age of Fantasy: Skirmish v3.6.0</em>, creación de bandas con ArmyForge o escenografía 3D disponible.
            </p>

            <div class="chat-box-feed" id="oracleChatFeed">
              <div class="chat-bubble bot">
                <strong>Oráculo Arcano:</strong> ¡Saludos, comandante! Estoy versado en las reglas oficiales de AoFS v3.6.0, en el catálogo de escenografía 3MF de nuestra campaña y en el balance de bandas. ¿Qué requieres esclarecer?
              </div>
            </div>

            <!-- Accesos rápidos -->
            <div style="display: flex; gap: 0.35rem; flex-wrap: wrap; margin-bottom: 0.6rem;">
              <button class="btn-action" style="font-size: 0.68rem; padding: 0.25rem 0.5rem;" onclick="app.askOraclePreset('acciones')">Acciones v3.6.0</button>
              <button class="btn-action" style="font-size: 0.68rem; padding: 0.25rem 0.5rem;" onclick="app.askOraclePreset('fatiga')">Fatiga Melé</button>
              <button class="btn-action" style="font-size: 0.68rem; padding: 0.25rem 0.5rem;" onclick="app.askOraclePreset('moral')">Chequeo 50%</button>
              <button class="btn-action" style="font-size: 0.68rem; padding: 0.25rem 0.5rem;" onclick="app.askOraclePreset('escenografia')">Escenografía 3D</button>
              <button class="btn-action" style="font-size: 0.68rem; padding: 0.25rem 0.5rem;" onclick="app.askOraclePreset('armyforge')">ArmyForge Bandas</button>
            </div>

            <div style="display: flex; gap: 0.5rem;">
              <input type="text" id="oracleQueryInput" class="form-control" placeholder="Escribe tu consulta arbitral..." onkeyup="if(event.key==='Enter') app.sendOracleQuery()"/>
              <button class="btn-action" onclick="app.sendOracleQuery()">
                <i class="fa-solid fa-paper-plane"></i>
              </button>
            </div>
          </div>

          <!-- Columna Derecha: Buzón de Sugerencias & Escenografía 3D -->
          <div class="panel-box">
            <h3 style="font-family: var(--font-gothic); font-size: 1.5rem; margin-bottom: 0.4rem;">
              <i class="fa-solid fa-inbox"></i> Buzón del Metajuego &amp; Escenografía 3D
            </h3>
            <p style="font-size: 0.82rem; color: var(--ink-muted); margin-bottom: 0.8rem;">
              Registra sugerencias de reglas de la casa, mejoras para la web o solicita piezas de escenografía para imprimir en 3D.
            </p>

            <form onsubmit="app.submitSuggestion(event)">
              <div style="margin-bottom: 0.6rem;">
                <label style="font-size: 0.75rem; font-weight: 800; font-family: var(--font-title);">Tipo de Sugerencia:</label>
                <select id="sugCategory" class="form-control">
                  <option value="Escenografía para Imprimir 3D">🖨️ Escenografía para Imprimir 3D</option>
                  <option value="Reglas de Campaña">⚔️ Reglas de Campaña / Casa</option>
                  <option value="Mejora de la WebApp">💻 Mejora de la WebApp</option>
                  <option value="Propuesta de Misión">📜 Propuesta de Escenario / Misión</option>
                </select>
              </div>

              <div style="margin-bottom: 0.6rem;">
                <label style="font-size: 0.75rem; font-weight: 800; font-family: var(--font-title);">Tu Sugerencia Detallada:</label>
                <textarea id="sugContent" class="form-control" placeholder="Describe tu propuesta, enlace STL o sugerencia para la campaña..." required></textarea>
              </div>

              <button type="submit" class="btn-action" style="margin-bottom: 1rem;">
                <i class="fa-solid fa-paper-plane"></i> Registrar en el Buzón
              </button>
            </form>

            <div style="border-top: 1px dashed var(--line-sepia); padding-top: 0.6rem;">
              <h4 style="font-family: var(--font-title); font-size: 0.82rem; font-weight: 800; margin-bottom: 0.4rem;">
                <i class="fa-solid fa-cubes"></i> Catálogo 3D Disponible (3MF):
              </h4>
              <ul style="font-size: 0.8rem; color: var(--ink-dark); line-height: 1.5; padding-left: 1.2rem;">
                <li><strong>Mansión en Ruinas (Building 4):</strong> 2 plantas, bloqueo de visión.</li>
                <li><strong>Ruinas Ulvheim (Placas 6 y 17):</strong> Arcos y parapetos modulares.</li>
                <li><strong>Casas Derruidas 2 y 3:</strong> Terreno difícil y cobertura gótica.</li>
                <li><strong>Cajas &amp; Barriles:</strong> Barricadas bajas con cobertura +1 salvación.</li>
                <li><strong>Bosque Tenebroso:</strong> Árboles marchitos para terreno exterior.</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- ======================================================== -->
      <!-- PESTAÑA 6: CONTACTO CON EL HERALDO (NPCS & ROLEPLAY)     -->
      <!-- ======================================================== -->
      <section class="tab-pane" id="tab-roleplay">
        <div class="panel-box">
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--ink-black); padding-bottom: 0.5rem; margin-bottom: 0.8rem;">
            <div>
              <h3 style="font-family: var(--font-gothic); font-size: 1.8rem; margin: 0;">
                <i class="fa-solid fa-comments"></i> Las Voces de la Ciudad Condenada
              </h3>
              <p style="font-size: 0.8rem; color: var(--ink-muted);">
                Interactúa con los supervivientes, fanáticos y granujas que merodean por Mordheim.
              </p>
            </div>
          </div>

          <!-- Selector de Personajes -->
          <div class="npc-selector-bar">
            <button class="npc-card-btn active" id="btnNpcGunter" onclick="app.selectNpc('gunter')">
              <span>🍺</span> Gunter «Tres-Dedos» (Tabernero)
            </button>
            <button class="npc-card-btn" id="btnNpcLothar" onclick="app.selectNpc('lothar')">
              <span>🕯️</span> Padre Lothar (Flagelante)
            </button>
            <button class="npc-card-btn" id="btnNpcSteinhardt" onclick="app.selectNpc('steinhardt')">
              <span>📜</span> Burgomaestre Von Steinhardt
            </button>
            <button class="npc-card-btn" id="btnNpcLoky" onclick="app.selectNpc('loky')">
              <span>🗡️</span> Loky el Desertor (Fugitivo R01)
            </button>
            <button class="npc-card-btn" id="btnNpcCronista" onclick="app.selectNpc('cronista')">
              <span>✒️</span> El Cronista Mayor
            </button>
          </div>

          <!-- Perfil del Personaje Activo -->
          <div style="background: #faf4e6; border: 1.5px solid var(--ink-black); padding: 0.75rem; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.8rem;">
            <span id="activeNpcAvatar" style="font-size: 2rem;">🍺</span>
            <div>
              <div id="activeNpcName" style="font-family: var(--font-title); font-weight: 800; font-size: 0.95rem; color: var(--ink-black);">Gunter «Tres-Dedos»</div>
              <div id="activeNpcDesc" style="font-size: 0.8rem; color: var(--ink-muted); font-style: italic;">Tuerto, desdentado y con un delantal sucio. Conoce todos los chismes de los arrabales.</div>
            </div>
          </div>

          <!-- Feed del Chat con el Personaje -->
          <div class="chat-box-feed" id="roleplayChatFeed" style="height: 340px;">
            <!-- Inyectado por JS -->
          </div>

          <!-- Entrada de Mensaje -->
          <div style="display: flex; gap: 0.5rem;">
            <input type="text" id="roleplayInput" class="form-control" placeholder="Escribe tu réplica o pregunta al personaje..." onkeyup="if(event.key==='Enter') app.sendRoleplayMessage()"/>
            <button class="btn-action" onclick="app.sendRoleplayMessage()">
              <i class="fa-solid fa-paper-plane"></i> Hablar
            </button>
          </div>
        </div>
      </section>

      <!-- ======================================================== -->
      <!-- PESTAÑA 7: PANEL GM DE DAVID (FOLIO 7)                   -->
      <!-- ======================================================== -->
      <section class="tab-pane" id="tab-gm">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem;">
          <!-- Ajustes de Campaña -->
          <div class="panel-box">
            <h3 style="font-family: var(--font-gothic); font-size: 1.6rem; color: var(--faction-david); margin-bottom: 0.6rem;">
              <i class="fa-solid fa-crown"></i> Control de Campaña (Solo Árbitro)
            </h3>

            <div style="margin-bottom: 1rem;">
              <label style="font-size: 0.75rem; font-weight: 800; font-family: var(--font-title);">Ronda Activa de Campaña:</label>
              <div style="display: flex; gap: 0.5rem; align-items: center; margin-top: 0.3rem;">
                <input type="number" id="gmRoundInput" class="form-control" style="width: 80px;" min="1" max="10" value="2"/>
                <button class="btn-action" onclick="app.updateGmRound()">Actualizar Ronda</button>
              </div>
            </div>

            <!-- Conexión Segura con Gemini API (Guardada en Supabase, nunca en Git) -->
            <div style="border: 1.5px solid var(--faction-david); background: #faf2f2; padding: 0.8rem; margin-bottom: 1rem;">
              <div style="font-family: var(--font-title); font-size: 0.75rem; font-weight: 800; color: var(--faction-david); margin-bottom: 0.3rem;">
                <i class="fa-solid fa-brain"></i> Configuración Inteligencia Artificial (Gemini)
              </div>
              <p style="font-size: 0.75rem; color: var(--ink-dark); margin-bottom: 0.4rem;">
                Guarda tu clave de Gemini aquí. Se almacena directamente en la base de datos de Supabase para que Sergio y Javi puedan hablar con los bots sin subir claves a GitHub.
              </p>
              <input type="password" id="geminiApiKeyInput" class="form-control" placeholder="AIzaSy..." style="margin-bottom: 0.4rem;"/>
              <button class="btn-action" onclick="app.saveGeminiKey()">
                <i class="fa-solid fa-floppy-disk"></i> Guardar en Supabase
              </button>
              <span id="geminiKeyStatus" style="font-size: 0.72rem; margin-left: 0.5rem; font-weight: 700;"></span>
            </div>

            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
              <button class="btn-action" onclick="app.saveState()">
                <i class="fa-solid fa-cloud-arrow-up"></i> Forzar Guardado en Nube
              </button>
              <button class="btn-action" onclick="app.rollD6Test()">
                <i class="fa-solid fa-dice-d6"></i> Tirar D6 de Campaña
              </button>
            </div>
            <div id="gmDiceResult" style="margin-top: 0.5rem; font-size: 0.85rem; font-weight: 800;"></div>
          </div>

          <!-- Sugerencias Recibidas de los Jugadores -->
          <div class="panel-box">
            <h3 style="font-family: var(--font-gothic); font-size: 1.6rem; color: var(--ink-black); margin-bottom: 0.6rem;">
              <i class="fa-solid fa-inbox"></i> Sugerencias del Tribunal
            </h3>
            <div id="gmSuggestionsList" style="max-height: 420px; overflow-y: auto; display: flex; flex-direction: column; gap: 0.6rem;">
              <!-- Inyectado por JS -->
            </div>
          </div>
        </div>
      </section>

    </main>

    <!-- PIE DE PÁGINA -->
    <footer class="gazette-footer">
      <div>
        <span>MORDHEIM: WAR ROOM v2.0 • OnePageRules: Age of Fantasy Skirmish</span>
      </div>
      <div class="sync-status">
        <div class="sync-dot" id="syncDot"></div>
        <span id="syncText">Conectando a Supabase...</span>
      </div>
    </footer>

  </div>

  <!-- SCRIPT ENGINE PRINCIPAL -->
  <script type="module">
    // 1. CONFIGURACIÓN SUPABASE & MEMORIA
    const SUPABASE_URL = "https://gwryzkejvymurjnyfwpu.supabase.co";
    const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3cnl6a2VqdnltdXJqbnlmd3B1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIxMjg1NDgsImV4cCI6MjA4NzcwNDU0OH0.x1PU7qnWJTLA5P6DO0Og6SlnSi0vIyTh98iu3GCk3fw";
    const STORAGE_KEY = "mordheim_warroom_v1";
    const SUGGESTIONS_KEY = "mordheim_sugerencias";
    const GEMINI_CONFIG_KEY = "mordheim_gemini_config";

    let supabase = null;
    if (window.supabase && SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
      } catch (err) {
        console.warn("Supabase init error:", err);
      }
    }

    // 2. CREDENCIALES & FACCIONES
    const USERS = {
      david: {
        id: "david",
        name: "David (Sangre Carmesí)",
        role: "Lord Sangriento & Game Master",
        faction: "Vampiric Undead",
        avatar: "🧛",
        color: "#7a1515",
        pin: "1348",
        isGm: true,
        secretOrder: {
          title: "Profanar la Capilla de las Almas",
          desc: "Tus nigromantes exigen recuperar el Libro de los Muertos enterrado bajo el mausoleo central.",
          reward: "+15 Coronas y Hechizo Menor Gratuito"
        }
      },
      sergio: {
        id: "sergio",
        name: "Sergio (Clan Scutrix)",
        role: "Señor de la Plaga",
        faction: "Ratmen",
        avatar: "🐀",
        color: "#1b4d24",
        pin: "6995",
        isGm: false,
        secretOrder: {
          title: "Asegurar el Altar Fluvial",
          desc: "Tus ingenieros deben capturar los conductos del Río Stir para verter gas de disformidad en las cloacas.",
          reward: "+20 Coronas de Oro"
        }
      },
      javi: {
        id: "javi",
        name: "Javi (Hijos del Yunque)",
        role: "Patriarca Minero",
        faction: "Dwarf Guilds",
        avatar: "⚒️",
        color: "#8a4f08",
        pin: "7788",
        isGm: false,
        secretOrder: {
          title: "Recuperar el Cofre del Gremio",
          desc: "Un antiguo arcón con lingotes de gromril yace bajo los escombros de la Forja de los Gremios.",
          reward: "Arma Rúnica Gratuita"
        }
      },
      spectator: {
        id: "spectator",
        name: "Espectador Neutral",
        role: "Forastero / Público",
        faction: "Neutral",
        avatar: "👁️",
        color: "#575249",
        pin: "",
        isGm: false,
        secretOrder: null
      }
    };

    // 3. MORDHEIM CARTOGRAFÍA (1077 x 794)
    const DISTRICTS = [
      {
        id: 1,
        numRoman: "I",
        name: "La Roca de Sigmar",
        owner: "sergio",
        perk: "Vigilancia Sacra: Permite desplegar 1 unidad con Scout a 12 pulgadas del despliegue base.",
        lore: "Monasterio insular en mitad del cauce del río Stir. Soportó la onda expansiva del cometa gracias a la devoción de sus defensoras.",
        x: 190, y: 395,
        icon: "fa-fort-awesome"
      },
      {
        id: 2,
        numRoman: "II",
        name: "El Cruce del Degollador",
        owner: "neutral",
        perk: "Rutas de Contrabando: Ingreso de +15 coronas de oro adicionales tras cada escaramuza.",
        lore: "Encrucijada exterior donde mercaderes sin escrúpulos compran esquirlas de piedra bruja.",
        x: 535, y: 125,
        icon: "fa-coins"
      },
      {
        id: 3,
        numRoman: "III",
        name: "La Forja de los Gremios",
        owner: "neutral",
        perk: "Maestría del Acero: Descuento permanente de 5 pts en cualquier mejora de arma.",
        lore: "Antiguos talleres de los artesanos y enanos imperiales. Aún quedan yunques intactos.",
        x: 760, y: 255,
        icon: "fa-hammer"
      },
      {
        id: 4,
        numRoman: "IV",
        name: "Las Criptas de Sylvania",
        owner: "david",
        perk: "Aura de Pavor: Una vez por partida, puedes forzar a una unidad enemiga a repetir un chequeo de moral superado.",
        lore: "Mausoleos profanados por la Casa Sangre Carmesí donde la niebla ponzoñosa jamás se disipa.",
        x: 325, y: 620,
        icon: "fa-skull"
      },
      {
        id: 9,
        numRoman: "IX",
        name: "El Pozo (The Pit)",
        owner: "neutral",
        perk: "Dominio de la Piedra Bruja: Concede +2 VP de campaña por ronda que se mantenga bajo control.",
        lore: "El abismo titánico donde el bólido de disformidad pulverizó el centro geográfico de Mordheim.",
        x: 540, y: 445,
        icon: "fa-meteor",
        isCentral: true
      },
      {
        id: 5,
        numRoman: "V",
        name: "El Gran Puente del Río Stir",
        owner: "neutral",
        perk: "Paso Estratégico: Elige automáticamente quién despliega 1º o 2º en sus batallas.",
        lore: "El viaducto de arcos de piedra que conecta el norte aristocrático con el sur obrero.",
        x: 500, y: 285,
        icon: "fa-archway"
      },
      {
        id: 6,
        numRoman: "VI",
        name: "La Torre del Alquimista",
        owner: "neutral",
        perk: "Elixires de Disformidad: +1 a tiradas de recuperación de heridas y supervivencia post-batalla.",
        lore: "Spira retorcida donde los sabios arcanos experimentaban antes de la catástrofe.",
        x: 275, y: 215,
        icon: "fa-flask-vial"
      },
      {
        id: 7,
        numRoman: "VII",
        name: "El Foso de los Escombros",
        owner: "neutral",
        perk: "Carroñeo de Ruinas: Tira 1D6 tras cada batalla: con 4+ encuentras equipo gratis valorado en 15 pts.",
        lore: "Laberinto de vigas caídas y sótanos reventados en el Distrito Bajo.",
        x: 825, y: 555,
        icon: "fa-box-open"
      },
      {
        id: 8,
        numRoman: "VIII",
        name: "El Laberinto de las Cloacas",
        owner: "neutral",
        perk: "Infiltración Murina: Permite a 1 unidad desplegar mediante la regla Ambush.",
        lore: "Dédalo subterráneo de aguas pútridas por donde los Hombres Rata emergen sin ser vistos.",
        x: 395, y: 395,
        icon: "fa-spider"
      }
    ];

    // 4. MISIONES
    const MISSIONS_DATA = {
      1: {
        id: 1,
        title: "Ronda 01: El Despertar del Colmillo de Hierro",
        badge: "COMPLETADA",
        badgeStyle: "background: #dfcb9f; color: #3a2e22; border: 1.5px solid #3a2e22;",
        rulebook: "AoF: Skirmish v3.6.0",
        points: "600 pts",
        turns: "4 Rondas",
        tableSize: "90x90 cm (David) / 120x120 cm (Sergio & Javi)",
        lore: "Tras el impacto del cometa sobre las cúpulas de Mordheim, las avanzadas de la Casa Sangre Carmesí y del Clan Scutrix se lanzaron a disputar el paso de La Roca de Sigmar y los muelles fluviales. El choque concluyó con la victoria de las ratas y la cobarde fuga de Loky.",
        objectives: [
          "Controlar La Roca de Sigmar al final de la Ronda 4 (+2 VP)",
          "Eliminar al Campeón o Héroe enemigo (+1 VP)",
          "Asegurar al menos 1 cofre de Piedra Bruja (+1 VP)"
        ]
      },
      2: {
        id: 2,
        title: "Ronda 02: La Caza de la Piedra Bruja en las Ruinas",
        badge: "RONDA EN CURSO",
        badgeStyle: "background: var(--faction-sergio-bg); color: var(--faction-sergio); border: 1.5px solid var(--faction-sergio);",
        rulebook: "AoF: Skirmish v3.6.0",
        points: "600 pts (+botín acumulado)",
        turns: "4 Rondas",
        tableSize: "90x90 cm (David) / 120x120 cm (Sergio & Javi)",
        lore: "Los ecos de la fuga de Loky aún resuenan en las tabernas de los arrabales. Tres filones de Piedra Bruja fosforescente han quedado al descubierto entre los escombros de la Plaza del Mercado y el Gran Puente del Río Stir. Las tres bandas se lanzan en una carrera desesperada para saquear los monolitos antes de que la niebla ponzoñosa los asfixie.",
        objectives: [
          "Recuperar esquirlas de Piedra Bruja (Marcadores de Objetivo: 3 repartidos) (+1 VP cada una)",
          "Expulsar a las bandas rivales del cuadrante central (+2 VP)",
          "Hacer que el líder enemigo chequee moral al 50% (+1 VP)"
        ]
      }
    };

    // 5. NPCS LORE DE MORDHEIM
    const NPCS = {
      gunter: {
        name: "Gunter «Tres-Dedos»",
        role: "Tabernero de Las Rocas",
        avatar: "🍺",
        desc: "Tuerto, desdentado y con un delantal manchado de cerveza y sangre seca. Conoce todos los chismes que se cuecen en los arrabales.",
        systemPrompt: "Eres Gunter 'Tres-Dedos', tabernero borracho y cínico de la taberna 'El Cerdo Degollado' en los arrabales de Mordheim (OPR Skirmish). Hablas con hipo (*hic*), jerga castiza y picaresca medieval, quejándote de que nadie paga la cerveza y vendiendo cotilleos de la fuga de Loky, las ratas de Scutrix y los vampiros. Respuestas sabrosas de 2 a 3 párrafos.",
        greeting: "¡*Hic*! Pasa, forastero... pero si no traes monedas o esquirlas de piedra verde para pagar la pinta de cerveza de nabos, date la vuelta. ¿Qué quieres saber de las ruinas?"
      },
      lothar: {
        name: "Padre Lothar",
        role: "Sacerdote Flagelante de Sigmar",
        avatar: "🕯️",
        desc: "Ojos inyectados en sangre, túnica rota y un mayal al cinto. Ve la mano del cometa como el castigo celestial a los impíos.",
        systemPrompt: "Eres el Padre Lothar, un sacerdote fanático y flagelante del culto a Sigmar en Mordheim. Hablas con fervor apocalíptico, condenando la soberbia de la ciudad y clamando que el cometa de dos colas cayó para purgar a los pecadores. Odias a los hechiceros, a los vampiros y a los hombres rata. Exiges penitencia. Respuestas de 2 a 3 párrafos.",
        greeting: "¡Arrepentíos! ¡El cometa de dos colas partió los cielos porque esta ciudad se revolcaba en la herejía! ¿Vienes a buscar la redención por el fuego o eres otro perro codicioso tras la piedra maldita?"
      },
      steinhardt: {
        name: "Burgomaestre Von Steinhardt",
        role: "Magistrado Imperial Exiliado",
        avatar: "📜",
        desc: "Viste ropajes de terciopelo raídos por la ceniza. Sostiene una pluma de ganso e intenta registrar la propiedad de una ciudad que ya no existe.",
        systemPrompt: "Eres el Burgomaestre Von Steinhardt, antiguo alto magistrado y recaudador de Mordheim. Eres formal, educado y angustiado. Intentas mantener el protocolo civil, la legalidad imperial y reclamar los libros de cuentas perdidos. Respuestas elegantes, melancólicas y burocráticas.",
        greeting: "Bienvenido a la cancillería de campaña, estimado conciudadano. Le ruego disculpe el estado de los archivos; el cataclismo ha desbaratado el registro fiscal. ¿Presenta credenciales o viene a declarar posesiones en los distritos?"
      },
      loky: {
        name: "Loky el Desertor",
        role: "Mercenario & Bribón Fugitivo",
        avatar: "🗡️",
        desc: "Oculto tras un pajar en El Cruce del Degollador. Sonríe con insolencia mientras mastica una brizna de paja.",
        systemPrompt: "Eres Loky, el infame mercenario que huyó en el carromato de víveres en la Batalla de la Ronda 01. Eres un canalla astuto, cobarde confeso y orgulloso de estar vivo: 'Un soldado muerto no cobra dos veces, camarada'. Te burlas de los héroes y justificas tu retirada con que tus mulas tenían más cabeza que los enanos y las ratas. Respuestas chispeantes y sarcásticas.",
        greeting: "¡Ssshh! ¡Baja la voz, condenado! Si Sergio o los enanos me ven por aquí me despellejan. Y que quede claro: ¡no fue una huida, fue una maniobra táctica de abastecimiento con mulas veloces! ¿Qué necesitas de Loky?"
      },
      cronista: {
        name: "El Cronista Mayor",
        role: "Redactor Jefe de El Heraldo",
        avatar: "✒️",
        desc: "Erudito y archivero de la imprenta imperial. Su pluma relata los hechos bélicos con objetividad histórica y rigor gótico.",
        systemPrompt: "Eres el Cronista Mayor de El Heraldo de Mordheim. Tu tono es solemne, de imprenta gótica del siglo XVI. Conoces la cronología del desastre, el valor de la piedra bruja y el estado de las facciones. Respuestas eruditas y evocadoras de 2 a 3 párrafos.",
        greeting: "Que la tinta conserve lo que el fuego y el acero amenazan con devorar. Soy el Cronista de El Heraldo. Preguntad sobre los anales de la ciudad o los partes de batalla."
      }
    };

    // 6. CLASE PRINCIPAL WARROOM APP
    class WarRoomApp {
      constructor() {
        this.currentUser = null;
        this.selectedDistrictId = 1;
        this.currentMissionId = 2;
        this.activeNpcKey = 'gunter';
        this.geminiApiKey = '';
        this.state = {
          round: 2,
          commanders: {
            david: { vp: 1, gold: 300 },
            sergio: { vp: 3, gold: 330 },
            javi: { vp: 0, gold: 300 }
          },
          districts: JSON.parse(JSON.stringify(DISTRICTS)),
          aars: [
            {
              id: "aar_1",
              author: "Sergio (Clan Scutrix)",
              opponent: "David (Sangre Carmesí)",
              result: "Victoria Decisiva (+2 VP)",
              text: "¡Victoria chillona para el Clan Scutrix! El gas de disformidad envolvió a los esqueletos y Queek lideró la carga sobre el Bastión Central antes de que los no-muertos reaccionaran.",
              time: "Ronda 01 • Encrucijada"
            },
            {
              id: "aar_2",
              author: "David (Sangre Carmesí)",
              opponent: "Sergio (Clan Scutrix)",
              result: "Derrota Táctica (+1 VP)",
              text: "La horda de roedores se abalanzó con frenesí ciego. Logramos decapitar al campeón Queek con nuestras garras antes de replegarnos con dignidad hacia las Catacumbas Reales.",
              time: "Ronda 01 • Criptas"
            }
          ],
          suggestions: []
        };
        this.loginSelectedUser = null;
        this.init();
      }

      async init() {
        this.setupNavigation();
        await this.loadCloudState();
        this.checkSavedSession();
      }

      checkSavedSession() {
        const saved = localStorage.getItem("mordheim_warroom_user");
        if (saved) {
          try {
            const parsed = JSON.parse(saved);
            if (USERS[parsed.id]) {
              this.currentUser = USERS[parsed.id];
              this.onUserLoggedIn();
              return;
            }
          } catch(e) {}
        }
        // Si no hay sesión, ir a pantalla de Login
        this.showTab('tab-login');
        this.updateUserChip();
      }

      selectLoginUser(userId) {
        this.loginSelectedUser = userId;
        document.querySelectorAll('.login-user-card').forEach(c => c.classList.remove('selected'));
        event.currentTarget.classList.add('selected');

        const box = document.getElementById("loginPinBox");
        const prompt = document.getElementById("loginPinPrompt");
        const err = document.getElementById("loginPinError");
        err.style.display = 'none';

        if (userId === 'spectator') {
          // Espectador entra directo sin PIN
          this.currentUser = USERS.spectator;
          localStorage.setItem("mordheim_warroom_user", JSON.stringify(this.currentUser));
          this.onUserLoggedIn();
        } else {
          box.style.display = 'block';
          prompt.textContent = `Introduce el PIN de ${USERS[userId].name}`;
          const input = document.getElementById("loginPinInput");
          input.value = '';
          input.focus();
        }
      }

      submitPin() {
        if (!this.loginSelectedUser) return;
        const input = document.getElementById("loginPinInput");
        const err = document.getElementById("loginPinError");
        const expected = USERS[this.loginSelectedUser].pin;

        if (input.value === expected) {
          err.style.display = 'none';
          this.currentUser = USERS[this.loginSelectedUser];
          localStorage.setItem("mordheim_warroom_user", JSON.stringify(this.currentUser));
          this.onUserLoggedIn();
        } else {
          err.style.display = 'block';
          input.value = '';
          input.focus();
        }
      }

      onUserLoggedIn() {
        document.getElementById("loginPinBox").style.display = 'none';
        this.updateUserChip();
        this.renderAll();
        // Por defecto activar El Heraldo (Pestaña 1)
        this.showTab('tab-gazette');
      }

      logout() {
        localStorage.removeItem("mordheim_warroom_user");
        this.currentUser = null;
        this.updateUserChip();
        this.showTab('tab-login');
      }

      updateUserChip() {
        const avatar = document.getElementById("userHeaderAvatar");
        const name = document.getElementById("userHeaderName");
        const gmTab = document.getElementById("tabGmBtn");
        const districtGmBox = document.getElementById("districtGmBox");

        if (this.currentUser) {
          avatar.textContent = this.currentUser.avatar;
          name.textContent = this.currentUser.name;
          if (this.currentUser.isGm) {
            gmTab.style.display = 'inline-flex';
            if (districtGmBox) districtGmBox.style.display = 'block';
          } else {
            gmTab.style.display = 'none';
            if (districtGmBox) districtGmBox.style.display = 'none';
          }
        } else {
          avatar.textContent = "👁️";
          name.textContent = "Sin Identificar";
          gmTab.style.display = 'none';
          if (districtGmBox) districtGmBox.style.display = 'none';
        }
      }

      setupNavigation() {
        document.querySelectorAll('.tab-btn').forEach(btn => {
          btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-tab');
            this.showTab(target);
          });
        });
      }

      showTab(tabId) {
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

        const pane = document.getElementById(tabId);
        if (pane) pane.classList.add('active');

        const btn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
        if (btn) btn.classList.add('active');

        window.scrollTo({ top: 0, behavior: 'smooth' });
      }

      async loadCloudState() {
        // Cargar estado de campaña
        if (supabase) {
          try {
            const { data, error } = await supabase
              .from('kv_store')
              .select('value')
              .eq('key', STORAGE_KEY)
              .maybeSingle();

            if (!error && data && data.value) {
              this.state = data.value;
              document.getElementById("syncDot").className = "sync-dot";
              document.getElementById("syncText").textContent = "Nube Conectada (Supabase 24/7)";
            } else if (!error && !data) {
              await supabase.from('kv_store').upsert({ key: STORAGE_KEY, value: this.state });
            }

            // Cargar API Key de Gemini
            const geminiRes = await supabase.from('kv_store').select('value').eq('key', GEMINI_CONFIG_KEY).maybeSingle();
            if (geminiRes.data && geminiRes.data.value && geminiRes.data.value.apiKey) {
              this.geminiApiKey = geminiRes.data.value.apiKey;
              const input = document.getElementById("geminiApiKeyInput");
              if (input) input.value = this.geminiApiKey;
              const status = document.getElementById("geminiKeyStatus");
              if (status) status.textContent = "✅ IA Conectada";
            }
          } catch (e) {
            console.warn("Supabase fetch error:", e);
            document.getElementById("syncDot").className = "sync-dot offline";
            document.getElementById("syncText").textContent = "Modo Local / Desconectado";
          }
        }
      }

      async saveState() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
        if (supabase) {
          try {
            await supabase.from('kv_store').upsert({ key: STORAGE_KEY, value: this.state });
            document.getElementById("syncDot").className = "sync-dot";
            document.getElementById("syncText").textContent = "Sincronizado en Supabase 24/7";
          } catch(e) {
            console.warn("Supabase save error:", e);
          }
        }
      }

      renderAll() {
        this.renderScoreboard();
        this.showGazette(2);
        this.showMission(2);
        this.renderMordheimMap();
        this.renderDistrictDetails(this.selectedDistrictId);
        this.renderFogOfWar();
        this.renderAarFeed();
        this.renderRoleplayGreeting();
        this.renderGmSuggestions();
      }

      renderScoreboard() {
        const grid = document.getElementById("scoreboardCardsGrid");
        if (!grid) return;
        grid.innerHTML = "";

        const distCounts = { david: 0, sergio: 0, javi: 0 };
        this.state.districts.forEach(d => {
          if (distCounts[d.owner] !== undefined) distCounts[d.owner]++;
        });

        const list = [
          { key: 'david', u: USERS.david, c: this.state.commanders.david },
          { key: 'sergio', u: USERS.sergio, c: this.state.commanders.sergio },
          { key: 'javi', u: USERS.javi, c: this.state.commanders.javi }
        ];

        list.forEach(item => {
          const card = document.createElement("div");
          card.className = `commander-card ${item.key}`;
          card.innerHTML = `
            <div class="cmd-header">
              <div class="cmd-identity">
                <span class="cmd-avatar">${item.u.avatar}</span>
                <div>
                  <div class="cmd-name">${item.u.name}</div>
                  <div class="cmd-faction">${item.u.faction}</div>
                </div>
              </div>
              <span style="font-size: 0.65rem; font-family: var(--font-title); font-weight: 800; background: #e8dcb9; padding: 0.15rem 0.4rem; border: 1px solid var(--ink-black);">
                ${item.u.role}
              </span>
            </div>
            <div class="cmd-stats">
              <div>
                <div class="stat-val" style="color: ${item.u.color};">${item.c.vp}</div>
                <div class="stat-lbl">Puntos Victoria</div>
              </div>
              <div>
                <div class="stat-val">${item.c.gold}</div>
                <div class="stat-lbl">Coronas Oro</div>
              </div>
              <div>
                <div class="stat-val">${distCounts[item.key] || 0}</div>
                <div class="stat-lbl">Baluartes</div>
              </div>
            </div>
          `;
          grid.appendChild(card);
        });
      }

      showGazette(editionNum) {
        document.querySelectorAll('.herald-nav .btn-action').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById(`btnGazette${editionNum}`);
        if (btn) btn.classList.add('active');

        const meta = document.getElementById("gazetteIssueMeta");
        const title = document.getElementById("gazetteLeadTitle");
        const sublead = document.getElementById("gazetteSublead");
        const leftCol = document.getElementById("gazetteLeftCol");
        const img = document.getElementById("gazetteMainImg");
        const caption = document.getElementById("gazetteImgCaption");
        const pdfLink = document.getElementById("gazettePdfLink");

        if (editionNum === 0) {
          meta.textContent = "Número 0 (Fundacional) • La Caída del Cometa de Dos Colas";
          title.textContent = "¡EL IMPACTO DEL COMETA Y LA CAÍDA DE MORDHEIM!";
          sublead.textContent = "LA GRAN METRÓPOLIS CALCINADA POR LA ESTRELLA ERRANTE";
          img.src = "./assets/portada_edicion_00.jpg";
          caption.textContent = "Xilografía Fundacional: El cometa de dos colas precipitándose sobre las cúpulas de Mordheim.";
          pdfLink.href = "./assets/El_Heraldo_de_mordheim_Edicion_00.pdf";
          leftCol.innerHTML = `
            <p style="margin-bottom: 10px;">
              <span class="drop-cap">E</span>l juicio anunciado por los astrónomos no fue un símbolo de gloria, sino la tumba de la mayor metrópolis imperial. En la víspera del nuevo milenio, el bólido celeste de mineral oscuro atravesó las nubes y pulverizó los palacios, hundiendo el centro geográfico en un abismo titánico conocido como <strong>El Pozo</strong>.
            </p>
            <p style="margin-bottom: 10px;">
              Una nube de ceniza sulfurosa y vapores mágicos asfixió a miles en sus lechos. De la roca vítrea brotan cristales de <strong>Piedra Bruja (Wyrdstone)</strong>: la manifestación física más letal y codiciada de la magia primigenia.
            </p>
            <p>
              Las puertas de Mordheim han sido clausuradas por mandato marcial, pero las partidas de guerra ya convergen desde todas las fronteras dispuestas a desgarrarse por una sola esquirla de poder primordial.
            </p>
          `;
        } else if (editionNum === 1) {
          meta.textContent = "Número 1 • Apertura de la Campaña Urbana";
          title.textContent = "EL DESPERTAR DE LA CIUDAD CONDENADA";
          sublead.textContent = "TRES HUESTES CONVERGEN HACIA LAS RUINAS";
          img.src = "./assets/portada_edicion_01.jpg";
          caption.textContent = "Xilografía de Época: Tres huestes convergiendo en las ruinas de Mordheim.";
          pdfLink.href = "./assets/El_Heraldo_de_mordheim_Edicion_01.pdf";
          leftCol.innerHTML = `
            <p style="margin-bottom: 10px;">
              <span class="drop-cap">L</span>a Ciudad Condenada ha abierto sus fauces. Tras meses de niebla ponzoñosa, los accesos a la metrópolis son disputados con furia sanguinaria. Tres señores de la guerra pugnan por el dominio del empedrado.
            </p>
            <p style="margin-bottom: 10px;">
              Los espías confirman que los <strong>Ratmen del Clan Scutrix</strong> han emergido de las cloacas para fortificarse en los accesos al río, mientras que los <strong>Vampiric Undead de la Casa Sangre Carmesí</strong> profanan los mausoleos de la nobleza con artes nigrománticas.
            </p>
            <p>
              Por su parte, los <strong>Dwarf Guilds de los Hijos del Yunque</strong> han jurado ante sus ancestros que cada caja fuerte enana expoliada será cobrada con sangre y fuego de plomo.
            </p>
          `;
        } else {
          meta.textContent = "Número 2 (Extraordinaria) • Tras la Batalla en el Bastión Central";
          title.textContent = "¡LA MASACRE Y LA FUGA DE LOKY!";
          sublead.textContent = "COBARDÍA HISTÓRICA EN LA ENCRUCIJADA";
          img.src = "./assets/portada_edicion_02.jpg";
          caption.textContent = "Xilografía Clandestina: La cobarde fuga de Loky en su carromato de mulas tras la refriega en la encrucijada.";
          pdfLink.href = "./assets/El_Heraldo_de_mordheim_Edicion_02.pdf";
          leftCol.innerHTML = `
            <p style="margin-bottom: 10px;">
              <span class="drop-cap">¡E</span>scándalo en los arrabales de Mordheim! Los mensajeros del Heraldo confirman la masacre en la Encrucijada. Mientras las garras vampíricas de Lord David decapitaban al campeón Queek del Clan Scutrix, el infame mercenario Loky abandonó el frente a todo galope.
            </p>
            <p style="margin-bottom: 10px;">
              A pesar de la cobardía de sus cuadros auxiliares, las ratas lograron asentar su dominio táctico sobre el Bastión Central, consolidando <strong>La Roca</strong> como bastión del Clan Scutrix (3 VP).
            </p>
            <p>
              La hueste no-muerta se ha replegado hacia <strong>Las Criptas de Sylvania</strong> jurando venganza nocturna, mientras los enanos completan sus plegarias y afilan los picos rúnicos para la Ronda 02.
            </p>
          `;
        }
      }

      showMission(roundNum) {
        document.querySelectorAll('.mission-nav-bar .btn-action').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById(`btnMission${roundNum}`);
        if (btn) btn.classList.add('active');

        const m = MISSIONS_DATA[roundNum];
        if (!m) return;

        document.getElementById("missionTitleDisplay").textContent = m.title;
        const badge = document.getElementById("missionStatusBadge");
        badge.textContent = m.badge;
        badge.style = m.badgeStyle;

        document.getElementById("missionRulebook").textContent = m.rulebook;
        document.getElementById("missionPoints").textContent = m.points;
        document.getElementById("missionTurns").textContent = m.turns;
        document.getElementById("missionTableSize").textContent = m.tableSize;
        document.getElementById("missionLoreText").textContent = m.lore;

        const ul = document.getElementById("missionObjectivesList");
        ul.innerHTML = "";
        m.objectives.forEach(obj => {
          const li = document.createElement("li");
          li.textContent = obj;
          ul.appendChild(li);
        });
      }

      renderMordheimMap() {
        const svg = document.getElementById("mordheimSvgMap");
        if (!svg) return;
        svg.innerHTML = "";

        this.state.districts.forEach(d => {
          let ringColor = "#8e806f";
          let fillColor = "rgba(87, 82, 73, 0.75)";
          if (d.owner === "david") { ringColor = "#ffd700"; fillColor = "rgba(122, 21, 21, 0.85)"; }
          if (d.owner === "sergio") { ringColor = "#73d13d"; fillColor = "rgba(27, 77, 36, 0.85)"; }
          if (d.owner === "javi") { ringColor = "#ffa940"; fillColor = "rgba(138, 79, 8, 0.85)"; }

          const isSelected = d.id === this.selectedDistrictId;
          const radius = d.isCentral ? 22 : 18;

          const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
          g.setAttribute("class", `map-pin ${isSelected ? 'active' : ''}`);
          g.setAttribute("transform", `translate(${d.x}, ${d.y})`);
          g.onclick = () => {
            this.selectedDistrictId = d.id;
            this.renderMordheimMap();
            this.renderDistrictDetails(d.id);
          };

          g.innerHTML = `
            ${isSelected ? `<circle r="${radius + 7}" fill="none" stroke="#241d17" stroke-width="2.5" stroke-dasharray="4 3"/>` : ""}
            <circle class="pin-ring" r="${radius + 2}" fill="none" stroke="${ringColor}" stroke-width="2"/>
            <circle r="${radius}" fill="${fillColor}" stroke="#17130e" stroke-width="2"/>
            <text y="5" fill="#ffffff" font-family="'Cinzel', serif" font-weight="900" font-size="${d.isCentral ? 13 : 11}" text-anchor="middle" filter="drop-shadow(1px 1px 1px rgba(0,0,0,0.8))">${d.numRoman}</text>
          `;
          svg.appendChild(g);
        });
      }

      renderDistrictDetails(id) {
        const d = this.state.districts.find(item => item.id === id);
        if (!d) return;

        document.getElementById("districtDetailNum").textContent = `DISTRITO ${d.numRoman}`;
        document.getElementById("districtDetailName").textContent = d.name;
        document.getElementById("districtDetailPerk").textContent = `«${d.perk}»`;
        document.getElementById("districtDetailLore").textContent = d.lore;

        const badge = document.getElementById("districtDetailBadge");
        if (d.owner === "david") {
          badge.style = "background: var(--faction-david-bg); color: var(--faction-david); border-color: var(--faction-david);";
          badge.textContent = "Control: David (Sangre Carmesí)";
        } else if (d.owner === "sergio") {
          badge.style = "background: var(--faction-sergio-bg); color: var(--faction-sergio); border-color: var(--faction-sergio);";
          badge.textContent = "Control: Sergio (Clan Scutrix)";
        } else if (d.owner === "javi") {
          badge.style = "background: var(--faction-javi-bg); color: var(--faction-javi); border-color: var(--faction-javi);";
          badge.textContent = "Control: Javi (Hijos del Yunque)";
        } else {
          badge.style = "background: var(--faction-neutral-bg); color: var(--faction-neutral); border-color: var(--faction-neutral);";
          badge.textContent = "Estado: Disputado (Neutral)";
        }
      }

      setDistrictOwner(ownerKey) {
        if (!this.currentUser || !this.currentUser.isGm) {
          alert("Solo el Árbitro David tiene autoridad para transferir soberanías.");
          return;
        }
        const d = this.state.districts.find(x => x.id === this.selectedDistrictId);
        if (d) {
          d.owner = ownerKey;
          this.renderMordheimMap();
          this.renderDistrictDetails(d.id);
          this.renderScoreboard();
          this.saveState();
        }
      }

      renderFogOfWar() {
        const box = document.getElementById("fogOfWarSecretBox");
        if (!box) return;

        if (!this.currentUser || this.currentUser.id === 'spectator') {
          box.innerHTML = `
            <div style="text-align: center; padding: 1.5rem 0.5rem; color: var(--ink-muted);">
              <i class="fa-solid fa-lock" style="font-size: 2rem; margin-bottom: 0.5rem; color: var(--line-sepia);"></i>
              <div style="font-family: var(--font-title); font-weight: 800; font-size: 0.85rem;">ACCESO RESTRINGIDO</div>
              <p style="font-size: 0.78rem; margin-top: 0.3rem;">Identifícate con tu facción para leer tus órdenes secretas de campamento.</p>
            </div>
          `;
          return;
        }

        const sec = this.currentUser.secretOrder;
        if (!sec) return;

        box.innerHTML = `
          <div style="font-family: var(--font-title); font-size: 0.88rem; font-weight: 800; color: ${this.currentUser.color}; margin-bottom: 0.3rem;">
            <i class="fa-solid fa-scroll"></i> ${sec.title}
          </div>
          <p style="font-size: 0.85rem; font-style: italic; color: var(--ink-dark); line-height: 1.45; margin-bottom: 0.6rem;">
            "${sec.desc}"
          </p>
          <div style="background: #faf4e6; border: 1px solid var(--ink-black); padding: 0.4rem 0.6rem; font-size: 0.78rem; font-family: var(--font-title);">
            <strong>Recompensa de Éxito:</strong> <span style="color: var(--faction-sergio); font-weight: 800;">${sec.reward}</span>
          </div>
        `;
      }

      // 7. PARTES DE GUERRA (AARs)
      submitAar(e) {
        e.preventDefault();
        const author = this.currentUser ? this.currentUser.name : "Comandante Anónimo";
        const opp = document.getElementById("aarOpponent").value;
        const res = document.getElementById("aarResult").value;
        const text = document.getElementById("aarStory").value;

        const newAar = {
          id: "aar_" + Date.now(),
          author: author,
          opponent: opp,
          result: res,
          text: text,
          time: `Ronda 0${this.state.round} • Mordheim`
        };

        this.state.aars.unshift(newAar);
        document.getElementById("aarStory").value = "";
        this.renderAarFeed();
        this.saveState();
        alert("⚔️ Despacho de guerra sellado y sincronizado en la nube.");
      }

      renderAarFeed() {
        const feed = document.getElementById("aarFeedContainer");
        if (!feed) return;
        feed.innerHTML = "";

        this.state.aars.forEach(item => {
          const div = document.createElement("div");
          div.style = "background: var(--bg-parchment-sheet); border: 1.5px solid var(--ink-black); padding: 0.75rem; box-shadow: 2px 2px 0 var(--ink-black);";
          div.innerHTML = `
            <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: var(--ink-muted); font-family: var(--font-title); font-weight: 800; border-bottom: 1px dashed var(--line-sepia); padding-bottom: 0.2rem; margin-bottom: 0.35rem;">
              <span><strong>${item.author}</strong> vs ${item.opponent}</span>
              <span>${item.time}</span>
            </div>
            <div style="font-size: 0.8rem; font-weight: 800; color: var(--faction-david); font-family: var(--font-title); margin-bottom: 0.3rem;">
              <i class="fa-solid fa-stamp"></i> ${item.result}
            </div>
            <p style="font-size: 0.88rem; font-style: italic; color: var(--ink-dark); line-height: 1.4;">«${item.text}»</p>
          `;
          feed.appendChild(div);
        });
      }

      // 8. EL ORÁCULO DEL METAJUEGO
      askOraclePreset(type) {
        const input = document.getElementById("oracleQueryInput");
        if (type === 'acciones') input.value = "¿Cuáles son las 4 acciones de activación en Skirmish v3.6.0?";
        if (type === 'fatiga') input.value = "¿Cómo funciona exactamente la fatiga en combate cuerpo a cuerpo?";
        if (type === 'moral') input.value = "¿Cuándo se chequea pánico al 50% de la banda?";
        if (type === 'escenografia') input.value = "¿Qué escenografía 3MF tenemos y qué cobertura da?";
        if (type === 'armyforge') input.value = "¿Cómo configurar la banda en ArmyForge para 600 puntos?";
        this.sendOracleQuery();
      }

      async sendOracleQuery() {
        const input = document.getElementById("oracleQueryInput");
        const query = input.value.trim();
        if (!query) return;

        const feed = document.getElementById("oracleChatFeed");
        // Bubble del usuario
        const userBubble = document.createElement("div");
        userBubble.className = "chat-bubble user";
        userBubble.innerHTML = `<strong>${this.currentUser ? this.currentUser.name : 'Comandante'}:</strong> ${query}`;
        feed.appendChild(userBubble);
        input.value = "";
        feed.scrollTop = feed.scrollHeight;

        // Bubble de pensando
        const botBubble = document.createElement("div");
        botBubble.className = "chat-bubble bot";
        botBubble.innerHTML = `<em>Consultando los grimorios arcanos...</em>`;
        feed.appendChild(botBubble);
        feed.scrollTop = feed.scrollHeight;

        // Intentar IA si hay clave guardada
        if (this.geminiApiKey) {
          try {
            const prompt = `Eres el Oráculo Arcano de Mordheim para el sistema de juego OnePageRules: Age of Fantasy Skirmish v3.6.0.
Conoces el reglamento oficial:
- Activación de una acción por turno: Hold (dispara completo), Advance (mueve 6 pulg. y dispara), Rush (mueve 12 pulg.), Charge (mueve 12 pulg. a contacto peana con peana para melé).
- Fatiga en melé: tras atacar, la unidad queda Fatigada hasta final de ronda (si vuelve a combatir solo impacta a 6s naturales).
- Moral al 50%: chequear Calidad. Fallo por disparo causa Shaken (acobardada). Fallo en melé tras perder el asalto causa Rout (baja definitiva).
- Cobertura da +1 a Defensa contra disparos. Trepar vertical hasta 3 pulg. gratis.
- Escenografía 3MF disponible: Mansión en ruinas (Building 4, 2 plantas), Ruinas Ulvheim (Placas 6 y 17 modulares), Casas derruidas 2 y 3, Muros caídos, Pilas de cajas y barriles (cobertura baja), Bosque tenebroso.
- Límites de banda: 600 pts en ArmyForge.
Responde de forma clara, precisa y ambientada en Mordheim. Consulta del jugador: "${query}"`;

            const resp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${this.geminiApiKey}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                contents: [{ parts: [{ text: prompt }] }]
              })
            });

            if (resp.ok) {
              const data = await resp.json();
              const reply = data.candidates[0].content.parts[0].text;
              botBubble.innerHTML = `<strong>Oráculo Arcano:</strong> ${reply.replace(/\\n/g, '<br>')}`;
              feed.scrollTop = feed.scrollHeight;
              return;
            }
          } catch(e) {
            console.warn("Gemini API call failed, using local rules KB:", e);
          }
        }

        // Fallback Base de Conocimiento Local
        setTimeout(() => {
          let ans = "No he hallado un veredicto exacto en los pergaminos inmediatos. Consulta el manual oficial de AoFS v3.6.0 o remite tu duda al Árbitro David en el Panel GM.";
          const q = query.toLowerCase();

          if (q.includes("accion") || q.includes("hold") || q.includes("rush") || q.includes("charge")) {
            ans = "<strong>Acciones en AoFS v3.6.0:</strong> Al activar una unidad eliges una acción:<br>• <strong>Hold:</strong> Quieto y dispara.<br>• <strong>Advance:</strong> Mueve 6 pulg. y dispara.<br>• <strong>Rush:</strong> Mueve 12 pulg. (sin disparo ni carga).<br>• <strong>Charge:</strong> Mueve 12 pulg. a contacto peana para combate cuerpo a cuerpo.";
          } else if (q.includes("fatiga") || q.includes("cac") || q.includes("cuerpo a cuerpo")) {
            ans = "<strong>Fatiga en Melé:</strong> Tras resolver sus ataques cuerpo a cuerpo, la unidad queda <em>Fatigada</em> hasta el final de la ronda completa. Si vuelve a combatir mientras esté fatigada, solo impactará con 6s naturales.";
          } else if (q.includes("moral") || q.includes("50") || q.includes("panico") || q.includes("shaken") || q.includes("rout")) {
            ans = "<strong>Chequeo de Moral al 50%:</strong> Cuando la banda queda al 50% o menos de miniaturas/vida, chequea Calidad:<br>• Fallo por disparo = <strong>Shaken (Acobardada)</strong>: no ataca ni mueve voluntariamente.<br>• Fallo tras perder un combate = <strong>Rout (Huida)</strong>: la miniatura es retirada como baja.";
          } else if (q.includes("escenografia") || q.includes("3mf") || q.includes("imprimir") || q.includes("terreno")) {
            ans = "<strong>Escenografía 3MF de Campaña:</strong><br>• <strong>Building 4:</strong> Mansión gótica de 2 plantas. Bloquea línea de visión y da altura.<br>• <strong>Ruinas Ulvheim (Placas 6 y 17):</strong> Muros con ventanas que otorgan +1 a cobertura.<br>• <strong>Cajas y Barriles:</strong> Cobertura baja.<br>• <strong>Bosque:</strong> Terreno difícil (-2 pulg. al avance).";
          } else if (q.includes("armyforge") || q.includes("lista") || q.includes("puntos") || q.includes("crear")) {
            ans = "<strong>Creación con ArmyForge:</strong> En la web de OPR ArmyForge selecciona <em>Age of Fantasy: Skirmish</em>. El presupuesto oficial de campaña es de <strong>600 puntos</strong> por banda, con un máximo de 1 Héroe y respetando el coste de equipo rúnico y magia.";
          }

          botBubble.innerHTML = `<strong>Oráculo Arcano:</strong> ${ans}`;
          feed.scrollTop = feed.scrollHeight;
        }, 300);
      }

      async submitSuggestion(e) {
        e.preventDefault();
        const cat = document.getElementById("sugCategory").value;
        const text = document.getElementById("sugContent").value;
        const author = this.currentUser ? this.currentUser.name : "Comandante";

        const newSug = {
          id: "sug_" + Date.now(),
          author: author,
          category: cat,
          content: text,
          date: new Date().toLocaleDateString('es-ES')
        };

        if (!this.state.suggestions) this.state.suggestions = [];
        this.state.suggestions.unshift(newSug);
        document.getElementById("sugContent").value = "";

        // Guardar en Supabase
        if (supabase) {
          try {
            await supabase.from('kv_store').upsert({ key: SUGGESTIONS_KEY, value: this.state.suggestions });
          } catch(e) {}
        }
        this.saveState();
        this.renderGmSuggestions();
        alert("📜 Sugerencia sellada y remitida al Buzón del Tribunal.");
      }

      // 9. CONTACTO CON EL HERALDO (NPCS & ROLEPLAY)
      selectNpc(npcKey) {
        this.activeNpcKey = npcKey;
        document.querySelectorAll('.npc-card-btn').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById(`btnNpc${npcKey.charAt(0).toUpperCase() + npcKey.slice(1)}`);
        if (btn) btn.classList.add('active');

        const npc = NPCS[npcKey];
        if (!npc) return;

        document.getElementById("activeNpcAvatar").textContent = npc.avatar;
        document.getElementById("activeNpcName").textContent = npc.name;
        document.getElementById("activeNpcDesc").textContent = npc.desc;

        this.renderRoleplayGreeting();
      }

      renderRoleplayGreeting() {
        const feed = document.getElementById("roleplayChatFeed");
        if (!feed) return;
        feed.innerHTML = "";

        const npc = NPCS[this.activeNpcKey];
        const bubble = document.createElement("div");
        bubble.className = "chat-bubble npc";
        bubble.innerHTML = `<strong>${npc.avatar} ${npc.name}:</strong> ${npc.greeting}`;
        feed.appendChild(bubble);
      }

      async sendRoleplayMessage() {
        const input = document.getElementById("roleplayInput");
        const msg = input.value.trim();
        if (!msg) return;

        const feed = document.getElementById("roleplayChatFeed");
        const userBubble = document.createElement("div");
        userBubble.className = "chat-bubble user";
        userBubble.innerHTML = `<strong>${this.currentUser ? this.currentUser.name : 'Tú'}:</strong> ${msg}`;
        feed.appendChild(userBubble);
        input.value = "";
        feed.scrollTop = feed.scrollHeight;

        const npc = NPCS[this.activeNpcKey];
        const npcBubble = document.createElement("div");
        npcBubble.className = "chat-bubble npc";
        npcBubble.innerHTML = `<em>${npc.avatar} ${npc.name} está respondiendo...</em>`;
        feed.appendChild(npcBubble);
        feed.scrollTop = feed.scrollHeight;

        // Si hay clave Gemini, llamar a la IA
        if (this.geminiApiKey) {
          try {
            const fullPrompt = `${npc.systemPrompt}
Estás hablando con: ${this.currentUser ? this.currentUser.name : 'un comandante forastero'}.
Mensaje que te acaba de decir: "${msg}".
Responde en perfecto personaje, manteniendo tu tono y referencias a los sucesos de Mordheim y la fuga de Loky.`;

            const resp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${this.geminiApiKey}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                contents: [{ parts: [{ text: fullPrompt }] }]
              })
            });

            if (resp.ok) {
              const data = await resp.json();
              const reply = data.candidates[0].content.parts[0].text;
              npcBubble.innerHTML = `<strong>${npc.avatar} ${npc.name}:</strong> ${reply.replace(/\\n/g, '<br>')}`;
              feed.scrollTop = feed.scrollHeight;
              return;
            }
          } catch(e) {
            console.warn("Roleplay AI call error:", e);
          }
        }

        // Fallback temático en personaje
        setTimeout(() => {
          let fallback = "";
          if (this.activeNpcKey === 'gunter') {
            fallback = "*Hic*... ¡No me vengas con ésas, forastero! Si quieres que te cuente lo que vi la noche que Loky huyó en el carro, pon otra moneda sobre la mesa. Dicen que las ratas del Clan Scutrix tienen túneles que cruzan por debajo de la mismísima taberna.";
          } else if (this.activeNpcKey === 'lothar') {
            fallback = "¡Necio! Las palabras mundanas no acallarán la cólera de Sigmar. Mira hacia el cielo ceniciento: el cometa partió las murallas porque los corazones estaban podridos. ¡Preparaos para la purga!";
          } else if (this.activeNpcKey === 'steinhardt') {
            fallback = "Anoto debidamente su declaración en los pliegos del distrito. No obstante, le advierto que hasta que el Tribunal restablezca el orden en el Gran Puente, las reclamaciones sobre las cajas de caudales deberán esperar a la Ronda 02.";
          } else if (this.activeNpcKey === 'loky') {
            fallback = "¡Bah! Dicen que huí, pero yo lo llamo 'retirada estratégica con preservación de víveres'. Mientras los fanáticos se rompían las cabezas contra los esqueletos, yo aseguré tres barriles intactos. Si quieres un socio para la Ronda 02, habla con mis mulas.";
          } else {
            fallback = "Las crónicas registrarán vuestras palabras, capitán. En las ruinas de Mordheim cada paso se paga con sangre y cada esquirla de piedra bruja forja una leyenda o una tumba anónima.";
          }
          npcBubble.innerHTML = `<strong>${npc.avatar} ${npc.name}:</strong> ${fallback}`;
          feed.scrollTop = feed.scrollHeight;
        }, 300);
      }

      // 10. PANEL GM (DAVID)
      updateGmRound() {
        const val = parseInt(document.getElementById("gmRoundInput").value, 10);
        if (val > 0) {
          this.state.round = val;
          document.getElementById("headerRoundTag").textContent = `RONDA 0${val} EN CURSO`;
          this.saveState();
          alert(`🏆 Campaña actualizada a la Ronda 0${val}.`);
        }
      }

      async saveGeminiKey() {
        const input = document.getElementById("geminiApiKeyInput");
        const key = input.value.trim();
        const status = document.getElementById("geminiKeyStatus");

        if (!key) {
          alert("Introduce una clave válida de Gemini.");
          return;
        }

        this.geminiApiKey = key;
        if (supabase) {
          try {
            await supabase.from('kv_store').upsert({ key: GEMINI_CONFIG_KEY, value: { apiKey: key } });
            status.textContent = "✅ Guardada en Supabase";
            alert("🔑 Clave de Gemini guardada de forma segura en la base de datos de la nube. Sergio y Javi ya pueden interactuar con los bots.");
          } catch(e) {
            status.textContent = "⚠️ Error al guardar";
          }
        }
      }

      rollD6Test() {
        const res = Math.floor(Math.random() * 6) + 1;
        const box = document.getElementById("gmDiceResult");
        box.innerHTML = `🎲 Resultado del D6 Arbitral: <span style="font-size: 1.2rem; color: var(--faction-david);">${res}</span>`;
      }

      renderGmSuggestions() {
        const list = document.getElementById("gmSuggestionsList");
        if (!list) return;
        list.innerHTML = "";

        const sugs = this.state.suggestions || [];
        if (sugs.length === 0) {
          list.innerHTML = `<div style="font-size: 0.8rem; color: var(--ink-muted); font-style: italic;">No hay sugerencias registradas todavía.</div>`;
          return;
        }

        sugs.forEach(s => {
          const item = document.createElement("div");
          item.style = "background: #faf4e6; border: 1px solid var(--ink-black); padding: 0.6rem; font-size: 0.82rem;";
          item.innerHTML = `
            <div style="display: flex; justify-content: space-between; font-weight: 800; font-family: var(--font-title); font-size: 0.72rem; color: var(--faction-david); margin-bottom: 0.2rem;">
              <span>${s.category} • ${s.author}</span>
              <span>${s.date}</span>
            </div>
            <p style="color: var(--ink-dark); font-style: italic;">«${s.content}»</p>
          `;
          list.appendChild(item);
        });
      }
    }

    // Instanciación Global
    window.app = new WarRoomApp();
  </script>
</body>
</html>
'''

with open(r'C:\Users\David\Desktop\Mordheim-WarRoom\index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("index.html generado con exito!")
