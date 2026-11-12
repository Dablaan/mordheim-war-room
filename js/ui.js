/**
 * Kar-Drakor: War Room — Interfaz y Renderizado de Componentes
 */
import { CONFIG } from './config.js';
import { AppState } from './state.js';

export const UI = {
    distritoSeleccionado: 1,

    init() {
        AppState.subscribe((state) => this.render(state));
        this.bindEvents();
        this.render(AppState);
    },

    bindEvents() {
        // Selector de Pestañas
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const targetTab = btn.getAttribute('data-tab');
                AppState.setPestaña(targetTab);
            });
        });

        // Cambio de Jugador (Click en user badge)
        document.getElementById('user-badge-btn').addEventListener('click', () => {
            this.abrirModalLogin();
        });

        // Formulario de Login
        document.querySelectorAll('.login-player-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const playerId = btn.getAttribute('data-player');
                if (playerId === 'david') {
                    const pin = prompt('Introduce el PIN de Game Master (1348):');
                    const res = AppState.login('david', pin);
                    if (!res.success) {
                        alert(res.error);
                        return;
                    }
                } else {
                    AppState.login(playerId);
                }
                this.cerrarModalLogin();
            });
        });

        // Tirada de Dado D6 para Bajas
        const btnDado = document.getElementById('btn-tirar-dado');
        if (btnDado) {
            btnDado.addEventListener('click', () => {
                const tirada = Math.floor(Math.random() * 6) + 1;
                let texto = '';
                if (tirada === 1) texto = `🎲 [${tirada}] 💀 MUERTO / DESTRUIDO (Baja definitiva de la banda)`;
                else if (tirada === 6) texto = `🎲 [${tirada}] ⚡ RECUPERADO CON VETERANÍA (+1 Calidad en Ronda 1)`;
                else texto = `🎲 [${tirada}] 🩹 RECUPERADO SIN SECUELAS (Listo para combatir)`;
                
                document.getElementById('resultado-dado').innerText = texto;
                const inputBajas = document.getElementById('input-parte-bajas');
                if (inputBajas) {
                    inputBajas.value += (inputBajas.value ? '\n' : '') + texto;
                }
            });
        }

        // Envío de Parte de Guerra
        const formParte = document.getElementById('form-parte-guerra');
        if (formParte) {
            formParte.addEventListener('submit', async (e) => {
                e.preventDefault();
                if (!AppState.jugadorActual || AppState.jugadorActual === 'espectador') {
                    alert('Debes identificarte como comandante para registrar un parte de guerra.');
                    this.abrirModalLogin();
                    return;
                }

                const parteData = {
                    jugador: AppState.jugadorActual,
                    rival: document.getElementById('input-parte-rival').value,
                    resultado: document.getElementById('input-parte-resultado').value,
                    vp: document.getElementById('input-parte-vp').value,
                    bajas: document.getElementById('input-parte-bajas').value,
                    relato: document.getElementById('input-parte-relato').value
                };

                await AppState.registrarParte(parteData);
                alert('⚔️ ¡Parte de guerra registrado en los anales de Kar-Drakor y sincronizado en la nube!');
                formParte.reset();
                document.getElementById('resultado-dado').innerText = '';
            });
        }

        // Chat del Oráculo con IA (Gemini)
        const btnEnviarOraculo = document.getElementById('btn-oraculo-enviar');
        const inputOraculo = document.getElementById('input-oraculo-texto');
        if (btnEnviarOraculo && inputOraculo) {
            const enviarMensaje = async () => {
                const txt = inputOraculo.value.trim();
                if (!txt) return;

                this.agregarMensajeOraculo('user', txt);
                inputOraculo.value = '';

                // Loader provisional
                const loaderId = this.agregarMensajeOraculo('oracle', '🔮 *El Oráculo consulta las cenizas rúnicas de Kar-Drakor...*');

                const respuesta = await AppState.consultarOraculo(txt);
                const elem = document.getElementById(loaderId);
                if (elem) elem.innerHTML = `<div class="oracle-bubble">${this.formatearMarkdown(respuesta)}</div>`;
            };

            btnEnviarOraculo.addEventListener('click', enviarMensaje);
            inputOraculo.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') enviarMensaje();
            });
        }
    },

    render(state) {
        if (!state.datos) return;

        this.renderUserBadge(state);
        this.renderNav(state);
        this.renderMarcador(state);
        this.renderMapa(state);
        this.renderDistritoDetalle(state);
        this.renderMision(state);
        this.renderPartes(state);
        this.renderHemeroteca(state);
        this.renderMasterPanel(state);
    },

    renderUserBadge(state) {
        const badgeElem = document.getElementById('user-badge-content');
        if (!badgeElem) return;

        if (!state.jugadorActual || state.jugadorActual === 'espectador') {
            badgeElem.innerHTML = `
                <i class="fa-solid fa-eye" style="color: #94a3b8;"></i>
                <div class="user-badge-name">Espectador <span style="font-size:0.7rem; color:var(--gold-bright);">(Cambiar)</span></div>
            `;
        } else {
            const jCfg = CONFIG.JUGADORES[state.jugadorActual];
            badgeElem.innerHTML = `
                <i class="fa-solid ${jCfg.emblema}" style="color: ${jCfg.color};"></i>
                <div>
                    <div class="user-badge-name" style="color:${jCfg.color}">${jCfg.nombre} ${jCfg.esMaster ? '⭐ (GM)' : ''}</div>
                    <div style="font-size:0.65rem; color:var(--text-muted);">${jCfg.banda}</div>
                </div>
            `;
        }
    },

    renderNav(state) {
        document.querySelectorAll('.nav-btn').forEach(btn => {
            const tab = btn.getAttribute('data-tab');
            if (tab === state.pestañaActiva) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }

            // Ocultar pestaña Master a quien no sea David
            if (tab === 'master') {
                btn.style.display = (state.jugadorActual === 'david') ? 'flex' : 'none';
            }
        });

        // Alternar paneles
        document.querySelectorAll('.tab-pane').forEach(pane => {
            if (pane.id === `tab-${state.pestañaActiva}`) {
                pane.classList.add('active');
            } else {
                pane.classList.remove('active');
            }
        });
    },

    renderMarcador(state) {
        const container = document.getElementById('scoreboard-container');
        if (!container) return;

        const m = state.datos.marcador;
        container.innerHTML = Object.keys(m).map(key => {
            const j = m[key];
            const cfg = CONFIG.JUGADORES[key];
            return `
                <div class="score-card faccion-${key}">
                    <div class="score-avatar" style="color: ${cfg.color}; background: ${cfg.colorBg};">
                        <i class="fa-solid ${j.icono}"></i>
                    </div>
                    <div class="score-info">
                        <div class="score-name">${j.nombre} <span style="font-size:0.75rem; color:var(--text-muted); font-weight:normal;">(${j.faccion})</span></div>
                        <div class="score-banda">${j.banda}</div>
                        <div class="score-stats">
                            <span class="stat-pill"><strong>${j.pv}</strong> VP</span>
                            <span class="stat-pill"><strong>${j.tesoreria}</strong> pts oro</span>
                            <span class="stat-pill"><strong>${j.distritos.length}</strong> distritos</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    },

    renderMapa(state) {
        const overlaySvg = document.getElementById('map-svg-lines');
        const nodesContainer = document.getElementById('map-nodes-container');
        if (!overlaySvg || !nodesContainer) return;

        // Dibujar líneas entre distritos
        const distMap = {};
        state.datos.distritos.forEach(d => { distMap[d.id] = d; });

        overlaySvg.innerHTML = state.datos.conexiones.map(([fromId, toId]) => {
            const from = distMap[fromId];
            const to = distMap[toId];
            if (!from || !to) return '';
            return `<line x1="${from.x}%" y1="${from.y}%" x2="${to.x}%" y2="${to.y}%" />`;
        }).join('');

        // Dibujar nodos de distritos
        nodesContainer.innerHTML = state.datos.distritos.map(dist => {
            const isSelected = this.distritoSeleccionado === dist.id;
            return `
                <div class="district-node control-${dist.control} ${isSelected ? 'selected' : ''}" 
                     style="left: ${dist.x}%; top: ${dist.y}%;"
                     onclick="window.seleccionarDistrito(${dist.id})">
                    <i class="fa-solid ${dist.icono}"></i>
                    <div class="district-label">${dist.id}. ${dist.nombre}</div>
                </div>
            `;
        }).join('');
    },

    renderDistritoDetalle(state) {
        const container = document.getElementById('district-detail-box');
        if (!container) return;

        const dist = state.datos.distritos.find(d => d.id === this.distritoSeleccionado) || state.datos.distritos[0];
        const duenio = CONFIG.JUGADORES[dist.control] || { nombre: 'Neutral / En Disputa', color: '#94a3b8', banda: 'Sin facción' };

        const esMaster = (state.jugadorActual === 'david');

        container.innerHTML = `
            <div class="district-detail-header">
                <div style="font-size:0.8rem; color:var(--text-gold); font-family:var(--font-heading);">Distrito Estratégico #${dist.id}</div>
                <h3 class="district-detail-title">${dist.nombre}</h3>
                <span class="district-detail-badge" style="background:${duenio.color}22; color:${duenio.color}; border: 1px solid ${duenio.color};">
                    Controlado por: <strong>${duenio.nombre}</strong> (${duenio.banda})
                </span>
            </div>

            <div>
                <div class="detail-section-title"><i class="fa-solid fa-scroll"></i> Trasfondo del Distrito</div>
                <p style="font-size:0.9rem; color:var(--text-muted); line-height:1.4;">${dist.descripcion}</p>
            </div>

            <div>
                <div class="detail-section-title"><i class="fa-solid fa-award"></i> Ventaja Estratégica de Control</div>
                <div class="advantage-box">${dist.ventaja}</div>
            </div>

            <div>
                <div class="detail-section-title"><i class="fa-solid fa-shield-halved"></i> Estado Operativo</div>
                <p style="font-size:0.85rem; color:#cbd5e1;">${dist.estado}</p>
            </div>

            ${esMaster ? `
                <div style="margin-top:10px; padding-top:14px; border-top:1px dashed var(--border-gold);">
                    <div class="detail-section-title" style="color:var(--gold-bright);"><i class="fa-solid fa-crown"></i> Control del Game Master</div>
                    <div style="display:flex; gap:8px; margin-top:8px;">
                        <button class="dice-btn" style="padding:6px 10px; font-size:0.75rem;" onclick="window.cambiarControlDistrito(${dist.id}, 'david')">Dar a David</button>
                        <button class="dice-btn" style="padding:6px 10px; font-size:0.75rem;" onclick="window.cambiarControlDistrito(${dist.id}, 'sergio')">Dar a Sergio</button>
                        <button class="dice-btn" style="padding:6px 10px; font-size:0.75rem;" onclick="window.cambiarControlDistrito(${dist.id}, 'javi')">Dar a Javi</button>
                        <button class="dice-btn" style="padding:6px 10px; font-size:0.75rem; background:#475569; color:#fff;" onclick="window.cambiarControlDistrito(${dist.id}, 'neutral')">Neutral</button>
                    </div>
                </div>
            ` : ''}
        `;
    },

    renderMision(state) {
        const mision = state.datos.misionRonda;
        const container = document.getElementById('mission-content-box');
        if (!container) return;

        container.innerHTML = `
            <div style="background:var(--bg-card); border:1px solid var(--border-gold); border-radius:var(--radius-lg); padding:24px; box-shadow:var(--shadow-epic);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <span style="font-family:var(--font-heading); color:var(--gold-bright); font-size:0.9rem;">Ronda Oficial ${mision.ronda}</span>
                    <a href="${mision.pdfUrl}" target="_blank" class="dice-btn" style="text-decoration:none; font-size:0.8rem; padding:6px 12px;">
                        <i class="fa-solid fa-file-pdf"></i> Descargar PDF Oficial
                    </a>
                </div>
                <h2 style="font-family:var(--font-heading); font-size:1.6rem; color:var(--text-gold); margin-bottom:8px;">${mision.titulo}</h2>
                <div style="display:flex; flex-wrap:wrap; gap:10px; margin-bottom:16px;">
                    <span class="stat-pill"><i class="fa-solid fa-chess-rook"></i> <strong>Escenario:</strong> ${mision.escenario}</span>
                    <span class="stat-pill"><i class="fa-solid fa-crosshairs"></i> <strong>Distrito:</strong> ${mision.distritoDisputa}</span>
                    <span class="stat-pill"><i class="fa-solid fa-shield"></i> <strong>Límite:</strong> ${mision.bandasPuntos}</span>
                    <span class="stat-pill"><i class="fa-solid fa-hourglass-half"></i> <strong>Duración:</strong> ${mision.duracion}</span>
                </div>
                <blockquote style="font-style:italic; color:var(--text-muted); border-left:3px solid var(--gold-bright); padding-left:14px; margin-bottom:20px; line-height:1.5;">
                    "${mision.lore}"
                </blockquote>

                <h4 style="font-family:var(--font-heading); color:var(--gold-bright); margin-bottom:8px;"><i class="fa-solid fa-map"></i> Plano Táctico de Mesa Recomendado</h4>
                <div style="margin-bottom:20px; border-radius:var(--radius-md); overflow:hidden; border:1px solid var(--border-gold);">
                    <img src="${mision.mapaImg}" alt="Plano de Mesa" style="width:100%; display:block;">
                </div>

                <h4 style="font-family:var(--font-heading); color:var(--gold-bright); margin-bottom:8px;"><i class="fa-solid fa-trophy"></i> Condiciones de Victoria y Botín</h4>
                <p style="font-size:0.95rem; line-height:1.5; color:#cbd5e1;">${mision.condiciones}</p>
            </div>
        `;

        // Renderizar Niebla de Guerra (Orden Secreta)
        const secretContainer = document.getElementById('secret-order-box');
        if (!secretContainer) return;

        const jugador = state.jugadorActual;
        if (!jugador || jugador === 'espectador') {
            secretContainer.innerHTML = `
                <div class="secret-order-card" style="text-align:center; padding:40px 20px;">
                    <i class="fa-solid fa-eye-slash" style="font-size:2.5rem; color:#8b5cf6; margin-bottom:14px;"></i>
                    <h3 style="font-family:var(--font-heading); color:#c4b5fd;">Niebla de Guerra Total</h3>
                    <p style="color:var(--text-muted); font-size:0.9rem; margin-top:8px;">Identifícate con tu facción para revelar las órdenes secretas que tus espías han interceptado en Kar-Drakor.</p>
                    <button class="dice-btn" style="margin:16px auto 0 auto;" onclick="window.UI.abrirModalLogin()">Identificar Comandante</button>
                </div>
            `;
        } else {
            const orden = state.datos.ordenesSecretas[jugador];
            const esGM = (jugador === 'david');
            secretContainer.innerHTML = `
                <div class="secret-order-card">
                    <span class="secret-badge"><i class="fa-solid fa-user-secret"></i> Confidencial</span>
                    <div style="font-size:0.8rem; color:#c4b5fd; font-family:var(--font-heading); margin-bottom:4px;">Orden Secreta de Campaña</div>
                    <h3 style="font-family:var(--font-heading); font-size:1.3rem; color:#f3e8ff; margin-bottom:12px;">${orden ? orden.titulo : 'Sin orden'}</h3>
                    <p style="font-size:0.9rem; color:#d8b4fe; font-style:italic; margin-bottom:14px; line-height:1.4;">"${orden ? orden.trasfondo : ''}"</p>
                    <div style="background:rgba(0,0,0,0.4); border-left:3px solid #8b5cf6; padding:10px 14px; border-radius:0 6px 6px 0; margin-bottom:12px;">
                        <strong style="color:#c4b5fd; font-family:var(--font-heading); font-size:0.85rem;">Objetivo Oculto:</strong>
                        <p style="font-size:0.9rem; color:#e9d5ff; margin-top:4px;">${orden ? orden.objetivo : ''}</p>
                    </div>
                    <div style="font-size:0.85rem; color:#a7f3d0;">
                        <i class="fa-solid fa-gift"></i> <strong>Recompensa Oculta:</strong> ${orden ? orden.recompensa : ''}
                    </div>

                    ${esGM ? `
                        <div style="margin-top:20px; padding-top:14px; border-top:1px dashed #8b5cf6; font-size:0.8rem; color:#c4b5fd;">
                            <i class="fa-solid fa-eye"></i> <strong>Visión GM:</strong> Como Game Master puedes auditar todas las órdenes secretas desde el Panel Master.
                        </div>
                    ` : ''}
                </div>
            `;
        }
    },

    renderPartes(state) {
        const feed = document.getElementById('partes-feed-container');
        if (!feed) return;

        feed.innerHTML = state.datos.partes.map(p => {
            const jCfg = CONFIG.JUGADORES[p.jugador] || { nombre: p.jugador, color: '#94a3b8', banda: '' };
            return `
                <div style="background:var(--bg-card); border:1px solid var(--border-gold); border-radius:var(--radius-md); padding:18px; margin-bottom:16px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <div>
                            <strong style="color:${jCfg.color}; font-family:var(--font-heading);">${jCfg.nombre} (${jCfg.banda})</strong>
                            <span style="font-size:0.8rem; color:var(--text-muted);">vs ${p.rival.toUpperCase()}</span>
                        </div>
                        <span class="stat-pill">Ronda ${p.ronda} — ${p.fecha}</span>
                    </div>
                    <div style="display:flex; gap:10px; margin-bottom:10px;">
                        <span class="stat-pill" style="border-color:${p.resultado.includes('Victoria') ? '#2b8a3e' : '#c92a2a'};">
                            <strong>${p.resultado}</strong>
                        </span>
                        <span class="stat-pill"><strong>+${p.vp}</strong> VP</span>
                    </div>
                    <div style="font-size:0.85rem; color:#f87171; margin-bottom:8px;">
                        <strong>Bajas / Secuelas:</strong> ${p.bajas || 'Ninguna'}
                    </div>
                    <blockquote style="font-style:italic; font-size:0.9rem; color:var(--text-muted); border-left:2px solid var(--border-gold); padding-left:12px; line-height:1.4;">
                        "${p.relato}"
                    </blockquote>
                </div>
            `;
        }).join('');
    },

    renderHemeroteca(state) {
        const container = document.getElementById('hemeroteca-container');
        if (!container) return;

        container.innerHTML = state.datos.periodicos.map(p => `
            <div class="gazette-card">
                <div class="gazette-header">
                    <div style="font-size:0.8rem; letter-spacing:3px; text-transform:uppercase;">Gaceta Oficial de las Ruinas</div>
                    <h2 class="gazette-name">EL HERALDO DE KAR-DRAKOR</h2>
                    <div style="font-size:0.85rem; color:#c5a059; margin-top:4px;">${p.titulo} • ${p.fecha}</div>
                </div>
                <div class="gazette-body">
                    <div>
                        <h3 style="font-family:'Cinzel', serif; font-size:1.3rem; margin-bottom:12px; color:#3b2d1d;">${p.titular}</h3>
                        <p style="font-size:0.95rem; line-height:1.6; color:#4a3f35; margin-bottom:18px;">${p.resumen}</p>
                        <a href="${p.pdf}" target="_blank" class="dice-btn" style="text-decoration:none; display:inline-flex;">
                            <i class="fa-solid fa-file-pdf"></i> Leer Edición Completa en PDF
                        </a>
                    </div>
                    <div>
                        <img src="${p.imagen}" alt="${p.titulo}" class="gazette-img">
                    </div>
                </div>
            </div>
        `).join('');
    },

    renderMasterPanel(state) {
        const container = document.getElementById('master-panel-content');
        if (!container) return;

        if (state.jugadorActual !== 'david') {
            container.innerHTML = `<p style="color:var(--text-muted); text-align:center;">Acceso restringido exclusivamente a Lord David (Game Master).</p>`;
            return;
        }

        container.innerHTML = `
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:24px;">
                <div style="background:var(--bg-card); border:1px solid var(--border-gold); padding:20px; border-radius:var(--radius-md);">
                    <h4 style="font-family:var(--font-heading); color:var(--gold-bright); margin-bottom:12px;"><i class="fa-solid fa-calendar-check"></i> Control de Ronda de Campaña</h4>
                    <label style="font-size:0.85rem; color:var(--text-gold);">Ronda Activa Actual:</label>
                    <select class="form-select" style="margin-top:6px; margin-bottom:14px;" onchange="window.AppState.setRonda(this.value)">
                        <option value="1" ${state.datos.rondaActual === 1 ? 'selected' : ''}>Ronda 1 — Asalto a la Puerta del Abismo</option>
                        <option value="2" ${state.datos.rondaActual === 2 ? 'selected' : ''}>Ronda 2 — Las Criptas y el Mercado</option>
                        <option value="3" ${state.datos.rondaActual === 3 ? 'selected' : ''}>Ronda 3 — La Grieta Umbría</option>
                        <option value="4" ${state.datos.rondaActual === 4 ? 'selected' : ''}>Ronda 4 — Criba por los Puntos de Victoria</option>
                        <option value="5" ${state.datos.rondaActual === 5 ? 'selected' : ''}>Ronda 5 — Desenlace en el Trono Hendido</option>
                    </select>
                </div>

                <div style="background:var(--bg-card); border:1px solid var(--border-gold); padding:20px; border-radius:var(--radius-md);">
                    <h4 style="font-family:var(--font-heading); color:var(--gold-bright); margin-bottom:12px;"><i class="fa-solid fa-database"></i> Sincronización & Respaldo Cloud</h4>
                    <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:14px;">El estado se sincroniza automáticamente con Supabase Cloud. Puedes forzar una copia local o restaurar.</p>
                    <button class="dice-btn" onclick="navigator.clipboard.writeText(JSON.stringify(window.AppState.datos, null, 2)); alert('¡Estado JSON copiado al portapapeles!');">
                        <i class="fa-solid fa-copy"></i> Copiar JSON de Campaña
                    </button>
                </div>
            </div>
        `;
    },

    agregarMensajeOraculo(remitente, texto) {
        const box = document.getElementById('oracle-chat-feed');
        if (!box) return null;

        const id = 'msg-' + Date.now();
        const msgHtml = `
            <div id="${id}" class="oracle-msg ${remitente}">
                <div class="oracle-bubble">
                    ${this.formatearMarkdown(texto)}
                </div>
            </div>
        `;
        box.insertAdjacentHTML('beforeend', msgHtml);
        box.scrollTop = box.scrollHeight;
        return id;
    },

    formatearMarkdown(txt) {
        return txt
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    },

    abrirModalLogin() {
        document.getElementById('modal-login').classList.add('active');
    },

    cerrarModalLogin() {
        document.getElementById('modal-login').classList.remove('active');
    }
};

// Funciones expuestas a eventos onclick globales
window.UI = UI;
window.seleccionarDistrito = (id) => {
    UI.distritoSeleccionado = id;
    UI.renderMapa(AppState);
    UI.renderDistritoDetalle(AppState);
};
window.cambiarControlDistrito = (id, nuevoDuenio) => {
    AppState.asignarDistrito(id, nuevoDuenio);
};
