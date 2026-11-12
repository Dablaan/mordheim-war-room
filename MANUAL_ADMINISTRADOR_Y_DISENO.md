# 📖 Manual Maestro del Administrador y Diseñador
## KAR-DRAKOR: WAR ROOM — Portal Web & Cuartel General de Campaña

> **Propósito de este documento**: Esta guía contiene toda la información técnica, arquitectónica, estética y operativa necesaria para que cualquier desarrollador, diseñador o director de juego ajeno al proyecto pueda comprenderlo al 100%, mantenerlo, modificar su diseño, añadir nuevas rondas o periódicos y administrar la campaña en la nube.

---

## 📌 1. Ficha Técnica y Enlaces del Proyecto

| Parámetro | Detalle / Enlace Oficial |
| :--- | :--- |
| **Aplicación Web en Vivo (24/7)** | [https://dablaan.github.io/kar-drakor-war-room/](https://dablaan.github.io/kar-drakor-war-room/) |
| **Repositorio Oficial de Código** | [https://github.com/Dablaan/kar-drakor-war-room](https://github.com/Dablaan/kar-drakor-war-room) |
| **Carpeta Local de Desarrollo** | `C:\Users\David\Desktop\Kar-Drakor-WarRoom\` |
| **Carpeta Original de Campaña (Obsidian)** | `Garbancito/30 Recursos/One Page Rules/Campaña Lidon/` |
| **Registro Central de Credenciales** | `Garbancito/20 Áreas/Gestión Digital/Registro_Central_APIs_y_Tokens.md` |
| **Sistema de Juego** | *Age of Fantasy: Skirmish* (v3.6.0) de OnePageRules (OPR) |
| **Hosting Cloud** | GitHub Pages (Despliegue serverless continuo desde rama `main`) |
| **Base de Datos Cloud** | Supabase PostgreSQL (`https://gwryzkejvymurjnyfwpu.supabase.co`) |

---

## 🏛️ 2. Origen y Filosofía del Proyecto

### ¿Por qué existe esta Web App?
Originalmente, la campaña se gestionaba mediante dos bots de Telegram que corrían en local mediante scripts de Python en el ordenador personal del Game Master (David). Esto provocaba dos problemas críticos:
1. **Pérdida de información**: El flujo continuo de chat sepultaba las misiones, el mapa, las reglas y los periódicos.
2. **Dependencia del PC encendido**: Si el ordenador de David se apagaba o suspendía, nadie podía consultar el estado ni registrar partes.

### La Solución "War Room"
Una aplicación web interactiva (PWA), adaptada a móviles y ordenadores, alojada gratuitamente en la nube 24/7 y conectada a Supabase. Permite:
* Gestionar el mapa de 9 distritos con un clic.
* Aplicar **niebla de guerra estricta** (cada jugador solo ve su misión secreta).
* Registrar partes de batalla con un **tirador interactivo 1D6 para la supervivencia de bajas**.
* Leer la gaceta *El Heraldo* con una maquetación renacentista inspirada en el legendario *Town Cryer* de Mordheim.
* Consultar dudas del reglamento oficial v3.6.0 mediante un oráculo inteligente.

---

## 🗺️ 3. Estructura de Archivos y Recursos

```text
Kar-Drakor-WarRoom/
├── index.html                           # Aplicación Web completa (HTML5 + CSS + JS Engine)
├── README.md                            # Resumen público del repositorio en GitHub
├── MANUAL_ADMINISTRADOR_Y_DISENO.md     # ESTE DOCUMENTO MAESTRO
├── css/
│   └── styles.css                       # Hoja de estilos complementaria / modular
├── js/
│   ├── config.js                        # Configuración de URLs, tokens y facciones
│   ├── data.js                          # Datos iniciales oficiales (9 distritos, marcador, órdenes)
│   ├── storage.js                       # Adaptador de persistencia Supabase + LocalStorage
│   ├── state.js                         # Gestor de estado reactivo
│   ├── ui.js                            # Renderizado dinámico de componentes
│   └── main.js                          # Script de arranque del motor modular
└── assets/                              # Recursos gráficos y documentos oficiales
    ├── Mapa_Kar_Drakor.png              # Plano táctico de fondo para la cartografía
    ├── Mapa_Mesa_90x90_Escaramuza.png   # Plano táctico de despliegue para la Ronda 1
    ├── El_Heraldo_de_Kar_Drakor_Edicion_01.png # Xilografía oficial de la Edición 01
    ├── El_Heraldo_de_Kar_Drakor_Edicion_01.pdf # PDF maquetado oficial de la Edición 01
    ├── El_Heraldo_de_Kar_Drakor_Edicion_02.png # Xilografía oficial de la Edición 02
    ├── El_Heraldo_de_Kar_Drakor_Edicion_02.pdf # PDF maquetado oficial de la Edición 02
    ├── Hoja_Mision_Ronda_01.pdf         # Hoja oficial de misión imprimible (2 páginas)
    └── Reglamento_Campana_Kar_Drakor.pdf # Reglamento oficial de campaña maquetado al estilo OPR
```

---

## 🎨 4. Guía del Diseñador (Estética, Estilos y Tipografías)

La estética visual de la web está inspirada en los panfletos y gacetas de guerra de finales del siglo XVI / principios del XVII, con la atmósfera *grimdark* de Warhammer Fantasy y Mordheim.

### 4.1. Tipografías Oficiales (Google Fonts)
Cargadas en la cabecera de `index.html`:
* **`UnifrakturMaguntia`**: Tipografía gótica Fraktur para grandes cabeceras maestras de periódicos (*El Heraldo*) y letras capitulares (`.drop-cap`).
* **`Pirata One`**: Tipografía rústica para subtítulos de gacetas y números de edición.
* **`Cinzel`**: Tipografía romana monumental para titulares de sección, nombres de facción y botones de acción.
* **`Playfair Display`**: Tipografía clásica con serifa para titulares de artículos y cartografía.
* **`EB Garamond`** e **`IM Fell DW Pica`**: Tipografías de imprenta antigua con serifa para lectura editorial y cuerpos de texto.

### 4.2. Paleta Cromática (Variables CSS en `:root`)
```css
--bg-parchment: #f6eedb;          /* Papel pergamino base */
--bg-parchment-sheet: #fff9ee;    /* Hoja limpia de imprenta */
--bg-parchment-dim: #ebdcb9;      /* Pergamino envejecido / botones inactivos */
--ink-black: #14110d;             /* Tinta negra de xilografía profunda */
--ink-dark: #221c15;              /* Tinta negra para lectura continua */
--ink-muted: #5e5345;             /* Tinta sepia para leyendas y metadatos */
--line-sepia: #9e8e78;            /* Líneas decorativas punteadas */

/* Colores de Facciones */
--faction-david: #7a1515;         /* Carmesí Sangre (David - Vampiric Undead) */
--faction-sergio: #1b4d24;        /* Verde Disformidad / Peste (Sergio - Ratmen) */
--faction-javi: #8a4f08;          /* Ámbar / Bronce de Forja (Javi - Dwarf Guilds) */
--faction-neutral: #575249;       /* Gris Pizarra (Distritos neutrales) */
```

### 4.3. Clases de Efecto Xilográfico y Papel
* `.newsprint-sheet`: Fondo con degradados radiales simulando manchas de humedad y envejecimiento del papel.
* `.border-woodcut-double`: Borde doble ancho característico de los grabados en madera medievales.
* `.woodcut-crop`: Filtro CSS (`grayscale(100%) contrast(145%) brightness(88%) sepia(30%) mix-blend-mode: multiply`) que transforma cualquier imagen moderna en una xilografía histórica impresa.
* `.drop-cap`: Letra capitular ornamental flotante para inicios de artículo.

---

## 👑 5. Guía del Administrador (Game Master / Árbitro)

### 5.1. Cómo identificarse como Game Master
1. Entra a la web: [https://dablaan.github.io/kar-drakor-war-room/](https://dablaan.github.io/kar-drakor-war-room/).
2. Haz clic en el escudo de identidad superior derecho.
3. Elige la opción **David (Casa Sangre Carmesí)**.
4. Introduce el **PIN de Game Master**: `1348`.
5. Aparecerá inmediatamente una corona dorada (`⭐ GM`) en la cabecera y se desbloquearán las funciones de arbitraje.

### 5.2. Herramientas del Administrador
* **Asignar Soberanía de Distritos**: En la pestaña *1. Cartografía Táctica*, haz clic en cualquier baluarte (I al IX). Al pie del panel lateral verás los botones del GM para transferir el control a David, Sergio, Javi o declararlo Neutral con un solo clic.
* **Control de Rondas**: En la pestaña *6. Panel GM*, puedes cambiar la ronda activa (de la 1 a la 5).
* **Gestión de Recursos**: Botones rápidos para otorgar `+20 de Oro` a todos los jugadores o `+1 VP` tras resolver una misión.
* **Auditoría de Niebla de Guerra**: Como Game Master, puedes auditar todas las órdenes secretas de los tres jugadores.
* **Copia de Seguridad JSON**: En el Panel GM puedes descargar con un clic el archivo `kardrakor_campaign_ronda_X.json` con el estado completo de la partida, o restaurar los valores iniciales.

---

## 🛠️ 6. Cómo Modificar y Añadir Nuevo Contenido

### 6.1. Cómo publicar una nueva Edición de "El Heraldo" (Ej: Edición 03)
1. Coloca la imagen de portada y el PDF oficial maquetado en la carpeta `assets/`:
   * `assets/El_Heraldo_de_Kar_Drakor_Edicion_03.png`
   * `assets/El_Heraldo_de_Kar_Drakor_Edicion_03.pdf`
2. Abre `index.html` y localiza la sección de la pestaña `#tab-gazette`.
3. Añade un botón selector para la nueva edición:
   ```html
   <button class="tab-btn" id="btnGazette3" onclick="app.showGazette(3)">Edición 03</button>
   ```
4. En el script de `index.html`, dentro de la función `showGazette(editionNum)`, añade el bloque condicional correspondiente:
   ```javascript
   else if (editionNum === 3) {
     b3.classList.add("active");
     // Desactivar las otras pestañas...
     meta.innerHTML = `<span>Número 3</span> • <span>Tras la Gran Escaramuza</span>`;
     title.textContent = "TITULAR EN MAYÚSCULAS DE LA EDICIÓN 3";
     sublead.textContent = "SUBTITULAR IMPACTANTE";
     deck.textContent = "Breve entradilla periodística en cursiva...";
     img.src = "./assets/El_Heraldo_de_Kar_Drakor_Edicion_03.png";
     caption.textContent = "Xilografía: Descripción del grabado...";
     pdfLink.href = "./assets/El_Heraldo_de_Kar_Drakor_Edicion_03.pdf";
     leftCol.innerHTML = `
       <p style="margin-bottom: 10px;">
         <span class="drop-cap">C</span>rónica redactada con letra capitular...
       </p>
     `;
   }
   ```

### 6.2. Cómo añadir nuevas reglas o preguntas frecuentes al Oráculo
En `index.html`, localiza la constante `RULES_KB`:
```javascript
const RULES_KB = [
  {
    keywords: ["palabra1", "palabra2", "disparo"],
    answer: "Explicación oficial del reglamento con formato <strong>HTML</strong>."
  },
  // Añadir aquí nuevos casos...
];
```

### 6.3. Cómo modificar los 9 Distritos o las Órdenes Secretas
Están definidos en el objeto `INITIAL_DATA` dentro de `index.html`:
* `INITIAL_DATA.districts`: Lista con id, número romano, nombre, coordenadas tácticas (`x`, `y`), propietario y ventaja de control (`perk`).
* `INITIAL_DATA.commanders[jugador].secretOrder`: Título, descripción y recompensa oculta de cada comandante.

---

## ☁️ 7. Flujo de Publicación en la Nube (Git & GitHub Pages)

Cualquier cambio realizado en la carpeta local `C:\Users\David\Desktop\Kar-Drakor-WarRoom\` se despliega en vivo en la nube en menos de 1 minuto siguiendo estos pasos en PowerShell:

```powershell
# 1. Acceder a la carpeta del proyecto
cd C:\Users\David\Desktop\Kar-Drakor-WarRoom

# 2. Comprobar archivos modificados
git status

# 3. Preparar los cambios
git add .

# 4. Crear commit con descripción clara
git commit -m "feat: publicacion de la edicion 03 de El Heraldo"

# 5. Enviar a GitHub
git push origin main
```

**¿Qué ocurre tras el push?**
* GitHub detecta el commit en la rama `main`.
* GitHub Pages compila y actualiza la web automáticamente en los servidores de GitHub (~30-45 segundos).
* Todos los jugadores verán el nuevo contenido al recargar [https://dablaan.github.io/kar-drakor-war-room/](https://dablaan.github.io/kar-drakor-war-room/).

---

## 🗄️ 8. Persistencia y Base de Datos (Supabase Cloud)

* **Servicio**: Supabase (PostgreSQL gratuito en la nube).
* **URL**: `https://gwryzkejvymurjnyfwpu.supabase.co`
* **Tabla**: `kv_store`
  * Columna `key` (`text`): `'kardrakor_warroom_v1'`
  * Columna `value` (`jsonb`): Almacena todo el estado activo (distritos, marcador, partes AAR y ronda).
* **Mecanismo de Salvaguarda**: Si un jugador entra sin conexión o falla la red, el código utiliza automáticamente `localStorage` como fallback transparente para que la aplicación nunca se bloquee. Al recuperar la red, se sincroniza con la nube.

---

*Documento redactado el 12 de Noviembre de 2026. Mantenido bajo la Cédula del Tribunal de Guerra de Kar-Drakor.*
