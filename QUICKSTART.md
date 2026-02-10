# 🚀 Guía Rápida de Inicio

## ⏱️ Configuración en 10 minutos

### Paso 1: Instalar Python (2 min)
1. Descargar Python 3.8+ desde https://www.python.org/downloads/
2. Durante la instalación, marcar "Add Python to PATH"
3. Verificar: `python --version`

### Paso 2: Instalar Tesseract OCR (3 min)

**Windows:**
1. Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Ejecutar instalador
3. Anotar ruta de instalación (ej: `C:\Program Files\Tesseract-OCR`)

**Linux:**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-spa
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

### Paso 3: Instalar dependencias Python (2 min)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar navegadores de Playwright
playwright install chromium
```

### Paso 4: Configurar MySQL (2 min)
```bash
# Conectar a MySQL
mysql -u root -p

# Ejecutar script de BD
mysql -u root -p < database_setup.sql
```

### Paso 5: Configurar credenciales (1 min)
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# Usar notepad, vim, nano, o cualquier editor
```

**Editar estas variables en .env:**
```env
DB_PASSWORD=tu_password_mysql
PLATFORM_URL=https://tu-plataforma.com
PLATFORM_USER=tu_usuario
PLATFORM_PASSWORD=tu_password
```

### Paso 6: Verificar instalación
```bash
python test_installation.py
```

### Paso 7: ¡Ejecutar!
```bash
python user_manager_app.py
```

---

## 🎯 Primer uso

### 1. Preparar una imagen de prueba
Crea un documento con este formato:

```
DATOS DEL USUARIO

Tipo de Documento: CC
Número: 1234567890
Nombre Completo: Juan Pérez García
Email: juan.perez@empresa.com
Rol: Administrador
Área: Tecnología
```

Guárdalo como imagen (PNG o JPG) con buena calidad.

### 2. Usar la aplicación

1. **Cargar imagen**: Clic en "Seleccionar Imagen"
2. **Procesar OCR**: Clic en "Extraer Datos (OCR)"
3. **Verificar datos**: Revisa y corrige si es necesario
4. **Consultar BD**: Opcional - verifica si existe
5. **Ejecutar acción**: Selecciona acción y ejecuta

---

## ⚙️ Configuración de selectores web

**BUENAS NOTICIAS:** El login ya está configurado con tus selectores de Playwright.

Solo necesitas configurar los selectores para gestión de usuarios.

### Herramienta de Playwright para generar selectores:

```bash
# Esto abre un navegador y graba tus acciones generando código
playwright codegen http://10.250.3.66:8080/savia
```

### Cómo encontrar selectores:

**Opción 1 - Codegen (Recomendado):**
1. Ejecuta `playwright codegen http://10.250.3.66:8080/savia`
2. Haz login manualmente
3. Ve a gestión de usuarios
4. Haz clic en los elementos que necesitas
5. Copia los selectores generados automáticamente

**Opción 2 - Manual:**
1. Abre tu plataforma en Chrome
2. Presiona `F12` (DevTools)
3. Usa inspector (Ctrl+Shift+C)
4. Clic en el elemento
5. Copia el selector

### Selectores en Playwright:

```python
# Por rol (MEJOR opción - más estable)
page.get_by_role("button", name="Guardar")

# Por texto visible
page.get_by_text("Editar")
page.locator("button:has-text('Guardar')")

# Por placeholder
page.get_by_placeholder("Buscar usuario...")

# Por CSS
page.locator("#btn-save")
page.locator(".btn-primary")

# Combinados (muy útil para tablas)
page.locator("tr:has-text('1234567890')").locator(".btn-edit")
```

### Ubicaciones a ajustar en `web_automation.py`:

Busca estos comentarios y ajusta según tu plataforma:
1. **Línea ~155:** Campo de búsqueda de usuarios
2. **Línea ~210:** Botón "Editar"
3. **Línea ~230:** Select de "Rol"
4. **Línea ~240:** Botón "Guardar"
5. **Línea ~285:** Botón "Desactivar"

**Ver guía completa:** `GUIA_SELECTORES.md`

---

## 🐛 Problemas comunes

### "Tesseract not found"
**Solución:** Agrega ruta en `ocr_processor.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### "Can't connect to MySQL"
**Solución:** 
```bash
# Verificar que MySQL esté corriendo
# Windows: Services > MySQL
# Linux: sudo systemctl status mysql
```

### "OCR no extrae correctamente"
**Solución:** 
- Usa imágenes de mejor calidad
- Asegúrate que el texto no esté rotado
- Prueba diferentes valores de preprocesamiento

### "Selenium no encuentra elementos"
**Solución:**
1. Ejecuta con `headless=False` para ver qué pasa
2. Verifica selectores con DevTools
3. Aumenta tiempos de espera

---

## 📊 Estructura de archivos

```
proyecto/
│
├── user_manager_app.py          ← Ejecutar esto
├── ocr_processor.py
├── database_handler.py
├── web_automation.py            ← Ajustar selectores aquí
│
├── requirements.txt
├── database_setup.sql
│
├── .env.example
├── .env                         ← Configurar credenciales aquí
│
├── README.md
├── QUICKSTART.md                ← Este archivo
└── test_installation.py
```

---

## ✅ Checklist de configuración

- [ ] Python 3.8+ instalado
- [ ] Tesseract OCR instalado
- [ ] MySQL/MariaDB instalado y corriendo
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Navegadores Playwright instalados (`playwright install chromium`)
- [ ] Base de datos creada (`database_setup.sql`)
- [ ] Archivo `.env` configurado con credenciales de BD
- [ ] Selectores web ajustados en `web_automation.py` (usa `playwright codegen` para ayuda)
- [ ] Test de instalación pasado (`python test_installation.py`)

---

## 🎓 Recursos adicionales

- **Documentación Playwright:** https://playwright.dev/python/
- **Generador de selectores:** `playwright codegen [URL]`
- **Documentación Tesseract:** https://tesseract-ocr.github.io/
- **Documentación MySQL:** https://dev.mysql.com/doc/
- **Tutorial Playwright:** https://playwright.dev/python/docs/intro

---

## 💡 Tips

1. **Mejora OCR:** Usa imágenes de 300+ DPI
2. **Seguridad:** Nunca subas `.env` a repositorios
3. **Testing:** Prueba con `headless=False` primero
4. **Logs:** Revisa el panel de logs para depurar
5. **Backup:** Respalda tu base de datos regularmente

---

## 🆘 ¿Necesitas ayuda?

1. Revisa README.md completo
2. Ejecuta `python test_installation.py`
3. Verifica logs de errores
4. Consulta sección "Solución de problemas" en README

---

**¡Listo para usar!** 🎉

Si todo está configurado correctamente:
```bash
python user_manager_app.py
```
