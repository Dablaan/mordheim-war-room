/**
 * Kar-Drakor: War Room - Gestor de Estado Reactivo
 */
import { CONFIG } from './config.js';
import { Storage } from './storage.js';

export const AppState = {
    // Jugador activo
    jugadorActual: null, // 'david' | 'sergio' | 'javi' | 'espectador'
    pestañaActiva: 'mapa', // 'mapa' | 'mision' | 'partes' | 'periodico' | 'oraculo' | 'master'

    // Datos de la campaña
    datos: null,

    // Suscriptores de UI
    listeners: [],

    /**
     * Inicializa el estado cargando datos desde la nube
     */
    async init() {
        this.datos = await Storage.loadState();
        
        // Recuperar última sesión de jugador si existe
        const sesionGuardada = localStorage.getItem('kardrakor_usuario_activo');
        if (sesionGuardada) {
            this.jugadorActual = sesionGuardada;
        }

        // Suscribirse a cambios en tiempo real desde Supabase
        Storage.subscribeRealtime((nuevosDatos) => {
            this.datos = nuevosDatos;
            this.notify();
        });

        this.notify();
    },

    /**
     * Registra un callback que se ejecuta cuando el estado cambia
     */
    subscribe(callback) {
        this.listeners.push(callback);
    },

    notify() {
        this.listeners.forEach(cb => cb(this));
    },

    /**
     * Autentica a un jugador
     */
    login(jugadorId, pin = null) {
        if (jugadorId === 'david') {
            if (pin !== CONFIG.MASTER_PIN) {
                return { success: false, error: 'PIN de Game Master incorrecto (Pista: 1348).' };
            }
        }
        this.jugadorActual = jugadorId;
        localStorage.setItem('kardrakor_usuario_activo', jugadorId);
        this.notify();
        return { success: true };
    },

    logout() {
        this.jugadorActual = null;
        localStorage.removeItem('kardrakor_usuario_activo');
        this.notify();
    },

    setPestaña(pestaña) {
        this.pestañaActiva = pestaña;
        this.notify();
    },

    /**
     * Asigna el control de un distrito
     */
    async asignarDistrito(distritoId, nuevoDuenio) {
        const dist = this.datos.distritos.find(d => d.id === distritoId);
        if (!dist) return;

        const viejoDuenio = dist.control;
        dist.control = nuevoDuenio;

        // Actualizar lista de distritos en el marcador
        Object.keys(this.datos.marcador).forEach(jKey => {
            const jugador = this.datos.marcador[jKey];
            jugador.distritos = this.datos.distritos.filter(d => d.control === jKey).map(d => d.id);
        });

        await Storage.saveState(this.datos);
        this.notify();
    },

    /**
     * Registra un nuevo parte de batalla
     */
    async registrarParte(parteData) {
        const nuevoParte = {
            id: 'parte-' + Date.now(),
            fecha: new Date().toISOString().split('T')[0],
            ronda: this.datos.rondaActual,
            jugador: parteData.jugador,
            rival: parteData.rival,
            resultado: parteData.resultado,
            vp: parseInt(parteData.vp) || 0,
            bajas: parteData.bajas,
            relato: parteData.relato
        };

        this.datos.partes.unshift(nuevoParte);

        // Sumar VP y ajustar marcador
        if (this.datos.marcador[parteData.jugador]) {
            this.datos.marcador[parteData.jugador].pv += nuevoParte.vp;
            this.datos.marcador[parteData.jugador].estado = `Último reporte: ${nuevoParte.resultado} vs ${parteData.rival}`;
        }

        await Storage.saveState(this.datos);
        this.notify();
        return nuevoParte;
    },

    /**
     * Avanza o cambia la ronda activa
     */
    async setRonda(nuevaRonda) {
        this.datos.rondaActual = parseInt(nuevaRonda);
        await Storage.saveState(this.datos);
        this.notify();
    },

    /**
     * Consulta al Oráculo de Reglas usando Gemini API
     */
    async consultarOraculo(pregunta) {
        const promptSystem = `
Eres el "Oráculo de Kar-Drakor", un árbitro experto e imparcial en el wargame "Age of Fantasy: Skirmish" (v3.6.0) de OnePageRules (OPR) y en la campaña narrativa "Las Cenizas de Kar-Drakor".
Reglas clave:
- Acciones: Hold (dispara), Advance (mueve 6" y dispara), Rush (mueve 12", sin disparar), Charge (mueve 12" a CaC).
- Combate: Calidad (Q) para impactar, Defensa (Def - AP) para bloquear.
- Fatiga en CaC: Atacar deja a la unidad Fatigada el resto de la ronda (impacta solo a 6s).
- Moral: Se chequea al 50% de vida o miniaturas. En disparo causa Shaken (acobardado), en CaC causa Rout (baja).
- Escenografía: Cobertura da +1 Def. Trepar hasta 3" verticales es gratis; más de 3" requiere chequeo de Calidad.
- Bajas post-batalla: 1=Muerto, 2-5=Recuperado, 6=Veterano (+1 Q en turno 1).
Responde de forma concisa, clara, con tono solemne de cronista medieval de fantasía oscura pero con precisión absoluta en las reglas. Si hay una regla dudosa, da la interpretación oficial de OPR.
        `;

        try {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${CONFIG.GEMINI_API_KEY}`;
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [
                        {
                            role: 'user',
                            parts: [{ text: `${promptSystem}\n\nPregunta del comandante: ${pregunta}` }]
                        }
                    ]
                })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error?.message || 'Error en la API de Gemini');
            }

            const data = await response.json();
            return data.candidates?.[0]?.content?.parts?.[0]?.text || 'El oráculo guarda silencio en las profundidades de la falla.';
        } catch (e) {
            console.error('Error en Oráculo Gemini:', e);
            // Fallback de reglas locales en caso de error de red o cuota
            return `📜 [Respuesta del Grimorio]: Las reglas básicas de AoFS dictan que las acciones son Hold, Advance (6"), Rush (12") o Charge (12"). Los chequeos de impacto usan Calidad (Q) y las salvaciones Defensa (Def - AP). Toda miniatura que ataque en melé queda Fatigada el resto de la ronda (solo impacta a 6s).`;
        }
    }
};
