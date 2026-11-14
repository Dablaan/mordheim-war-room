/**
 * Mordheim: War Room — Script Principal
 */
import { AppState } from './state.js';
import { UI } from './ui.js';

window.AppState = AppState;

document.addEventListener('DOMContentLoaded', async () => {
    console.log('⚔️ Iniciando Mordheim: War Room...');
    
    // Inicializar estado reactivo
    await AppState.init();

    // Inicializar interfaz
    UI.init();

    // Cerrar modal al hacer clic en el backdrop
    const modal = document.getElementById('modal-login');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                UI.cerrarModalLogin();
            }
        });
    }

    console.log('🏰 Cuartel General de Mordheim listo.');
});
