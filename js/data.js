/**
 * Kar-Drakor: War Room - Datos Iniciales de Campaña
 */
export const INITIAL_DATA = {
    rondaActual: 1,
    ultimaActualizacion: new Date().toISOString(),

    // Marcador de Campaña tras Ronda 1
    marcador: {
        sergio: {
            nombre: 'Sergio',
            banda: 'Clan Scutrix',
            faccion: 'Ratmen',
            pv: 3,
            tesoreria: 330,
            distritos: [1],
            bajas: 'Queek + 2 Alimañas',
            icono: 'fa-paw',
            color: '#2b8a3e',
            estado: 'Victoria en el Bastión Central'
        },
        david: {
            nombre: 'David',
            banda: 'Casa Sangre Carmesí',
            faccion: 'Vampiric Undead',
            pv: 1,
            tesoreria: 315,
            distritos: [4],
            bajas: 'Nigromante + 3 Esqueletos',
            icono: 'fa-skull',
            color: '#c92a2a',
            estado: 'Mención de Honor (Ejecutor de Queek)'
        },
        javi: {
            nombre: 'Javi',
            banda: 'Hijos del Yunque Ancestral',
            faccion: 'Dwarf Guilds',
            pv: 0,
            tesoreria: 300,
            distritos: [],
            bajas: 'Ninguna (en reserva táctica)',
            icono: 'fa-hammer',
            color: '#d97706',
            estado: 'Atrincherado en búnker exterior'
        }
    },

    // 9 Distritos de Kar-Drakor con coordenadas tácticas (% en el mapa)
    distritos: [
        {
            id: 1,
            nombre: 'La Puerta del Abismo',
            control: 'sergio',
            x: 20, // % horizontal
            y: 25, // % vertical
            icono: 'fa-dungeon',
            descripcion: 'La colosal entrada a la fortaleza en la superficie. Losas enanas desmoronadas y monolitos caídos.',
            ventaja: 'Vigilancia Exterior: Permite desplegar 1 unidad con la regla Scout en cualquier escenario.',
            estado: 'Bajo control del Clan Scutrix tras la batalla por el Bastión.'
        },
        {
            id: 2,
            nombre: 'El Mercado de las Sombras',
            control: 'neutral',
            x: 48,
            y: 18,
            icono: 'fa-coins',
            descripcion: 'Callejuelas de antiguos mercaderes ahora saqueadas. Bóvedas derruidas repletas de chatarrería de valor.',
            ventaja: 'Rutas Comerciales: La banda recibe +20 pts de oro/tesorería al finalizar cada ronda.',
            estado: 'Zona neutral en disputa. Disponible para Ronda 02.'
        },
        {
            id: 3,
            nombre: 'La Fragua Rúnica',
            control: 'neutral',
            x: 78,
            y: 22,
            icono: 'fa-fire',
            descripcion: 'Los hornos de los maestros herreros enanos aún tibios. Yunques rúnicos que conservan el secreto del acero.',
            ventaja: 'Maestría del Acero: Descuento permanente de 5 pts en cualquier mejora de arma que compres.',
            estado: 'Neutral. Objetivo prioritario en la mira de los Enanos.'
        },
        {
            id: 4,
            nombre: 'Las Catacumbas Reales',
            control: 'david',
            x: 22,
            y: 52,
            icono: 'fa-skull-crossbones',
            descripcion: 'Sepulcros sellados de los antiguos reyes y señores de la guerra. Magia nigromántica latente.',
            ventaja: 'Aura de Pavor: Una vez por partida, puedes forzar a una unidad enemiga a repetir un chequeo de moral superado.',
            estado: 'Bajo dominio de la Casa Sangre Carmesí tras el repliegue táctico.'
        },
        {
            id: 5,
            nombre: 'El Puente de los Juramentos',
            control: 'neutral',
            x: 50,
            y: 48,
            icono: 'fa-archway',
            descripcion: 'Paso colgado sobre el vacío que une los sectores norte y sur de la gran falla geológica.',
            ventaja: 'Posición Táctica: El poseedor elige automáticamente quién despliega primero o segundo en sus batallas.',
            estado: 'Paso libre sin guarnición defensiva.'
        },
        {
            id: 6,
            nombre: 'La Torre del Alquimista',
            control: 'neutral',
            x: 82,
            y: 50,
            icono: 'fa-flask',
            descripcion: 'Laboratorios repletos de reactivos humeantes, alambiques de cobre y elixires olvidados.',
            ventaja: 'Viales Restauradores: +1 a las tiradas de recuperación de heridas y supervivencia post-batalla de toda la banda.',
            estado: 'Neutral. Reactivos y frascos intactos.'
        },
        {
            id: 7,
            nombre: 'La Fosa de los Despojos',
            control: 'neutral',
            x: 18,
            y: 78,
            icono: 'fa-bone',
            descripcion: 'Vertedero de chatarra, restos bélicos y osamentas sin sepultura arrojadas al pozo.',
            ventaja: 'Carroñeo Constante: Tira 1D6 tras cada batalla: con 4+ encuentras equipo adicional valorado en 15 pts gratis.',
            estado: 'Neutral. Terreno de carroñeros y alimañas.'
        },
        {
            id: 8,
            nombre: 'El Nido del Pozo Negro',
            control: 'neutral',
            x: 50,
            y: 78,
            icono: 'fa-biohazard',
            descripcion: 'Laberinto de cloacas y conductos de ventilación en los estratos más profundos.',
            ventaja: 'Infiltración: Permite a una unidad desplegar mediante la regla Ambush.',
            estado: 'Conductos infestados pero sin dominio formal.'
        },
        {
            id: 9,
            nombre: 'El Gran Salón del Trono Hendido',
            control: 'neutral',
            x: 80,
            y: 80,
            icono: 'fa-crown',
            descripcion: 'El corazón soberano de Kar-Drakor, fracturado en dos por la Falla. El Trono de Hierro espera rey.',
            ventaja: 'Dominio Supremo: Concede +2 VP de Campaña por ronda que se mantenga bajo control.',
            estado: 'Sellado en las profundidades de la fortaleza.'
        }
    ],

    // Conexiones de rutas entre distritos
    conexiones: [
        [1, 2], [1, 4],
        [2, 3], [2, 5],
        [4, 5], [4, 7],
        [3, 6],
        [5, 8],
        [6, 9],
        [7, 8],
        [8, 9]
    ],

    // Misión Oficial Activa (Ronda 1)
    misionRonda: {
        ronda: 1,
        titulo: 'El Asalto a la Puerta del Abismo',
        escenario: 'Seize Ground (Tomar Terreno) — Pág. 22 AoFS',
        distritoDisputa: '1. La Puerta del Abismo',
        bandasPuntos: '300 puntos (máx. 1 Héroe)',
        duracion: '4 Rondas de juego (o muerte súbita)',
        lore: 'El suelo tembló cuando los antiguos portones de piedra enana de Kar-Drakor cedieron. Ahora, sobre una meseta sembrada de losas fracturadas y monolitos caídos, la vanguardia de los Vampiric Undead y la avanzadilla de los Ratmen chocan por el control de la única entrada transitable.',
        mesa: '4x4 pies (120x120 cm) o mesa 90x90 cm con 4 marcadores de objetivo en los cuadrantes.',
        condiciones: 'Control de Marcadores a 3" sin enemigos. Ganador: +2 VP de Campaña + 60 pts tesorería + control del Distrito 1. Perdedor: +120 pts tesorería de recuperación.',
        pdfUrl: 'assets/Hoja_Mision_Ronda_01.pdf',
        mapaImg: 'assets/Mapa_Mesa_90x90_Escaramuza.png'
    },

    // Órdenes Secretas (Niebla de Guerra por Jugador)
    ordenesSecretas: {
        david: {
            jugador: 'David',
            titulo: '«La Cosecha de la Primera Sangre»',
            trasfondo: 'Los ancestros susurran desde la piedra quebrada. Para asentar vuestro dominio necromántico sobre la Puerta del Abismo, necesitáis profanar el terreno antes de que los roedores envenenen el subsuelo.',
            objetivo: 'Termina la partida controlando al menos un marcador de objetivo en la mitad enemiga de la mesa, o destruye al menos 1 unidad enemiga en combate cuerpo a cuerpo con tu Vampiro/Héroe.',
            recompensa: '+1 VP de Campaña adicional y +15 pts de tesorería ocultos.'
        },
        sergio: {
            jugador: 'Sergio',
            titulo: '«Veneno en las Raíces»',
            trasfondo: 'Los videntes de la plaga exigen probar los nuevos gases y venenos en la carne muerta. Los vampiros creen que su magia es invulnerable, pero el ácido y la pólvora roedora pudren cualquier tejido.',
            objetivo: 'Sé el primer jugador en destruir por completo una unidad enemiga, o consigue que al menos dos unidades enemigas queden Acobardadas (Shaken) en la misma ronda por disparos o hechizos.',
            recompensa: '+1 VP de Campaña adicional y +15 pts de tesorería de botín hurtado.'
        },
        javi: {
            jugador: 'Javi',
            titulo: '«Reconocimiento de Agravios»',
            trasfondo: 'Los clanes de ingenieros han enviado exploradores hacia las lindes de Kar-Drakor. Se han detectado movimientos de blasfemos chupasangres e inmundas alimañas.',
            objetivo: 'Durante tu incursión de reconocimiento o primera escaramuza, mantén al menos el 50% de tus unidades intactas y asegura que tu Héroe sobreviva ileso al final del combate.',
            recompensa: '+1 VP de Campaña por disciplina táctica y +15 pts de tesorería de un alijo ancestral enano.'
        }
    },

    // Hemeroteca de El Heraldo
    periodicos: [
        {
            edicion: 2,
            titulo: 'Edición Extraordinaria: La Fuga de Loky y el Choque en la Encrucijada',
            fecha: 'Ronda 1 — Noviembre 2026',
            titular: '¡MASACRE EN EL BASTIÓN CENTRAL Y COBARDÍA HISTÓRICA!',
            resumen: 'Crónica del sangriento duelo entre Lord David y las hordas del Clan Scutrix. El infame Loky huyó en el carromato de víveres dejando a sus hermanos a merced de los colmillos no-muertos.',
            imagen: 'assets/El_Heraldo_de_Kar_Drakor_Edicion_02.png',
            pdf: 'assets/El_Heraldo_de_Kar_Drakor_Edicion_02.pdf'
        },
        {
            edicion: 1,
            titulo: 'Edición Inaugural: El Despertar del Colmillo de Hierro',
            fecha: 'Apertura de Campaña — Noviembre 2026',
            titular: '¡LA GRAN FALLA SE ABRE: CUATROCIENTOS AÑOS DE SILENCIO ROTOS!',
            resumen: 'Tres señores de la guerra convergen hacia las ruinas de Kar-Drakor. El pregonero de la fortaleza publica el bando oficial de reclutamiento y las reglas de conquista de los 9 distritos.',
            imagen: 'assets/El_Heraldo_de_Kar_Drakor_Edicion_01.png',
            pdf: 'assets/El_Heraldo_de_Kar_Drakor_Edicion_01.pdf'
        }
    ],

    // Historial acumulado de crónicas y partes de guerra
    partes: [
        {
            id: 'parte-1',
            fecha: '2026-11-09',
            ronda: 1,
            jugador: 'sergio',
            rival: 'david',
            resultado: 'Victoria',
            vp: 3,
            bajas: 'Queek (recuperado con 4+) + 2 Alimañas',
            relato: '¡Victoria chillona para el Clan Scutrix! El gas de disformidad envolvió a los esqueletos y Queek lideró la carga sobre el Bastión Central antes de que los no-muertos reaccionaran.'
        },
        {
            id: 'parte-2',
            fecha: '2026-11-09',
            ronda: 1,
            jugador: 'david',
            rival: 'sergio',
            resultado: 'Derrota Táctica',
            vp: 1,
            bajas: 'Nigromante (recuperado) + 3 Esqueletos destruidos',
            relato: 'La horda de roedores se abalanzó con frenesí ciego. Logramos decapitar al campeón Queek con nuestras garras vampíricas antes de replegarnos con dignidad hacia las Catacumbas Reales.'
        }
    ]
};
