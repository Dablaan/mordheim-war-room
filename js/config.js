/**
 * Mordheim: War Room - Configuración de Servicios Cloud
 */
export const CONFIG = {
    // Supabase Cloud Persistence (reutilizando la instancia del usuario)
    SUPABASE_URL: 'https://gwryzkejvymurjnyfwpu.supabase.co',
    SUPABASE_ANON_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3cnl6a2VqdnltdXJqbnlmd3B1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIxMjg1NDgsImV4cCI6MjA4NzcwNDU0OH0.x1PU7qnWJTLA5P6DO0Og6SlnSi0vIyTh98iu3GCk3fw',
    STORAGE_KEY: 'mordheim_warroom_v1',

    // Google Gemini API para el Oráculo de Reglas
    GEMINI_API_KEY: '',
    GEMINI_MODEL: 'gemini-2.5-flash',

    // Clave de acceso del Game Master
    MASTER_PIN: '1348',

    // Perfiles de Jugadores
    JUGADORES: {
        david: {
            id: 'david',
            nombre: 'David',
            titulo: 'Lord Sangriento & Game Master',
            faccion: 'Vampiric Undead',
            banda: 'Casa Sangre Carmesí',
            color: '#c92a2a',
            colorBg: 'rgba(201, 42, 42, 0.15)',
            emblema: 'fa-skull',
            esMaster: true
        },
        sergio: {
            id: 'sergio',
            nombre: 'Sergio',
            titulo: 'Señor del Clan Scutrix',
            faccion: 'Ratmen',
            banda: 'Clan Scutrix',
            color: '#2b8a3e',
            colorBg: 'rgba(43, 138, 62, 0.15)',
            emblema: 'fa-paw',
            esMaster: false
        },
        javi: {
            id: 'javi',
            nombre: 'Javi',
            titulo: 'Patriarca de las Forjas',
            faccion: 'Dwarf Guilds',
            banda: 'Hijos del Yunque Ancestral',
            color: '#d97706',
            colorBg: 'rgba(217, 119, 6, 0.15)',
            emblema: 'fa-hammer',
            esMaster: false
        }
    }
};
