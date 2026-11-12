/**
 * Kar-Drakor: War Room - Adaptador de Almacenamiento Cloud (Supabase + LocalStorage Fallback)
 */
import { CONFIG } from './config.js';
import { INITIAL_DATA } from './data.js';

let supabaseClient = null;

// Inicializar cliente de Supabase si la librería está cargada
if (window.supabase && CONFIG.SUPABASE_URL && CONFIG.SUPABASE_ANON_KEY) {
    try {
        supabaseClient = window.supabase.createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);
    } catch (e) {
        console.warn('No se pudo inicializar Supabase client:', e);
    }
}

export const Storage = {
    /**
     * Carga el estado de la campaña desde Supabase Cloud con fallback a localStorage
     */
    async loadState() {
        // 1. Intentar cargar desde Supabase
        if (supabaseClient) {
            try {
                const { data, error } = await supabaseClient
                    .from('kv_store')
                    .select('value')
                    .eq('key', CONFIG.STORAGE_KEY)
                    .maybeSingle();

                if (!error && data && data.value) {
                    console.log('✅ Estado cargado desde Supabase Cloud');
                    localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(data.value));
                    return data.value;
                }

                if (!error && !data) {
                    // Inicializar por primera vez en Supabase
                    console.log('⚡ Inicializando Kar-Drakor en Supabase por primera vez...');
                    await this.saveState(INITIAL_DATA);
                    return INITIAL_DATA;
                }
            } catch (err) {
                console.warn('Fallo al conectar con Supabase, usando almacenamiento local:', err);
            }
        }

        // 2. Fallback a LocalStorage
        try {
            const local = localStorage.getItem(CONFIG.STORAGE_KEY);
            if (local) {
                console.log('📂 Estado cargado desde LocalStorage');
                return JSON.parse(local);
            }
        } catch (e) {
            console.error('Error leyendo LocalStorage:', e);
        }

        // 3. Fallback inicial
        return INITIAL_DATA;
    },

    /**
     * Guarda el estado de la campaña tanto en Supabase como en LocalStorage
     */
    async saveState(stateData) {
        stateData.ultimaActualizacion = new Date().toISOString();

        // 1. Guardar en local siempre de inmediato
        try {
            localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(stateData));
        } catch (e) {
            console.error('Error guardando en LocalStorage:', e);
        }

        // 2. Guardar en Supabase Cloud
        if (supabaseClient) {
            try {
                const { error } = await supabaseClient
                    .from('kv_store')
                    .upsert({
                        key: CONFIG.STORAGE_KEY,
                        value: stateData
                    });

                if (error) {
                    console.error('Error guardando en Supabase:', error);
                } else {
                    console.log('☁️ Sincronizado en Supabase Cloud correctamente');
                }
            } catch (err) {
                console.error('Excepción guardando en Supabase:', err);
            }
        }
    },

    /**
     * Suscripción en tiempo real a cambios en Supabase (si otro jugador actualiza un parte o el GM cambia un distrito)
     */
    subscribeRealtime(onRemoteUpdate) {
        if (!supabaseClient) return;

        try {
            supabaseClient
                .channel('kardrakor-changes')
                .on(
                    'postgres_changes',
                    {
                        event: '*',
                        schema: 'public',
                        table: 'kv_store',
                        filter: `key=eq.${CONFIG.STORAGE_KEY}`
                    },
                    (payload) => {
                        console.log('🔔 Cambio en tiempo real detectado desde la nube:', payload);
                        if (payload.new && payload.new.value) {
                            onRemoteUpdate(payload.new.value);
                        }
                    }
                )
                .subscribe();
        } catch (e) {
            console.warn('Realtime subscription no disponible:', e);
        }
    }
};
