# ⚔️ Kar-Drakor: War Room (Portal Web de Campaña)
## Cuartel General 100% Online para Age of Fantasy: Skirmish (v3.6.0)

Este proyecto es la **Web App / PWA independiente** de la campaña narrativa *"Las Cenizas de Kar-Drakor"*. Resuelve definitivamente los cuellos de botella de Telegram:
1. **Cero pérdida de información**: Los 9 distritos, marcador de VP, fichas, hemeroteca de periódicos y misiones tienen su lugar fijo y permanente.
2. **Cero dependencia del PC encendido**: El portal corre en la nube (Vercel / GitHub Pages) conectado a la base de datos PostgreSQL de **Supabase Cloud**, funcionando 24/7 de forma autónoma.
3. **Niebla de guerra total**: Cada comandante ve exclusivamente sus órdenes secretas de la ronda al identificarse.
4. **Oráculo de Reglas con IA**: Árbitro de reglas integrado con Google Gemini API para responder dudas de AoFS v3.6.0 al instante.

---

## 🚀 Cómo Probarlo en Local

Puedes abrirlo de tres formas muy sencillas:

### Opción 1: Con Python (Servidor local ultrarrápido)
Abre una terminal PowerShell en esta carpeta y ejecuta:
```powershell
python -m http.server 8080
```
Y abre en tu navegador: `http://localhost:8080`

### Opción 2: Con la extensión Live Server de VS Code / Antigravity
Haz clic derecho en `index.html` y pulsa **"Open with Live Server"**.

---

## ☁️ Cómo Desplegarlo 100% Online en la Nube (Gratis y Permanente)

### Opción A: Despliegue en GitHub Pages (Recomendada y en 2 minutos)
1. Crea un nuevo repositorio en tu cuenta de GitHub (`Dablaan/kar-drakor-war-room`).
2. En esta carpeta ejecuta:
   ```powershell
   git init
   git add .
   git commit -m "feat: Lanzamiento de Kar-Drakor War Room"
   git branch -M main
   git remote add origin https://github.com/Dablaan/kar-drakor-war-room.git
   git push -u origin main
   ```
3. En GitHub ve a **Settings > Pages** y activa `Deploy from branch: main / (root)`.
4. ¡Listo! Tendrás tu enlace permanente accesible desde cualquier móvil: `https://dablaan.github.io/kar-drakor-war-room/`

### Opción B: Despliegue en Vercel
1. Ve a [vercel.com](https://vercel.com).
2. Conecta tu repositorio de GitHub `Dablaan/kar-drakor-war-room`.
3. Haz clic en **Deploy**. Tendrás dominio gratuito con HTTPS y CDN mundial instantáneo.

---

## 🔐 Credenciales y Configuración Central
Las claves y conexiones a Supabase y Gemini API están centralizadas en `js/config.js` y documentadas en tu bóveda de Obsidian en:
`20 Áreas/Gestión Digital/Registro_Central_APIs_y_Tokens.md`
