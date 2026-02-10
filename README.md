# 🔐 Sistema de Gestión de Usuarios con OCR

Aplicación de escritorio con interfaz gráfica para automatizar la gestión de usuarios mediante extracción de datos desde imágenes (OCR) e interacción con plataforma web.

## 📋 Funcionalidades

- ✅ **Extracción de datos** desde imágenes usando OCR
- ✅ **Consulta de usuarios** en base de datos MySQL
- ✅ **Cambio de roles** de usuarios en plataforma web
- ✅ **Desactivación de usuarios** en plataforma web
- ✅ **Interfaz gráfica intuitiva** con Tkinter
- ✅ **Sistema de logs** para rastrear operaciones

## 🎯 Datos que se extraen de las imágenes

- Tipo de documento (CC, CE, TI, PA, etc.)
- Número de documento
- Nombre completo
- Email/Usuario
- Rol/Perfil
- Área/Departamento

## 🛠️ Requisitos previos

### 1. Python
- Python 3.8 o superior
- Descargar desde: https://www.python.org/downloads/

### 2. Tesseract OCR
**Windows:**
- Descargar instalador desde: https://github.com/UB-Mannheim/tesseract/wiki
- Instalar y anotar la ruta (ej: `C:\Program Files\Tesseract-OCR`)
- Agregar Tesseract al PATH del sistema

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

**macOS:**
```bash
brew install tesseract
```

### 3. ChromeDriver / Playwright
- Playwright se instala con pip y descarga los navegadores automáticamente
- Después de instalar las dependencias, ejecutar:
```bash
playwright install chromium
```

### 4. MySQL/MariaDB
- MySQL 8.0+ o MariaDB 10.5+
- Descargar desde: https://dev.mysql.com/downloads/

## 📦 Instalación

### Paso 1: Clonar o descargar el proyecto

```bash
cd tu_directorio
```

### Paso 2: Crear entorno virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Instalar navegadores de Playwright

```bash
playwright install chromium
```

Este comando descarga Chromium para que Playwright pueda usarlo.

### Paso 5: Configurar base de datos

1. Conectarse a MySQL:
```bash
mysql -u root -p
```

2. Ejecutar script de base de datos:
```bash
mysql -u root -p < database_setup.sql
```

O copiar y pegar el contenido de `database_setup.sql` en tu cliente MySQL.

### Paso 6: Configurar variables de entorno

1. Copiar archivo de ejemplo:
```bash
cp .env.example .env
```

2. Editar `.env` con tus credenciales:
```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_NAME=usuarios_db
DB_USER=root
DB_PASSWORD=tu_contraseña

# Plataforma web SAVIA (ya preconfigurada)
PLATFORM_URL=http://10.250.3.66:8080/savia
PLATFORM_USER=dpiedrar
PLATFORM_PASSWORD=i0BnXmZr
```

### Paso 7: Ajustar selectores web

**IMPORTANTE:** El login ya está configurado con tus selectores. Solo necesitas ajustar los selectores para la gestión de usuarios en `web_automation.py`.

**Consulta la guía detallada:** `GUIA_SELECTORES.md`

Abre `web_automation.py` y busca los comentarios `# AJUSTA EL SELECTOR`.

Ejemplos de selectores en Playwright:
```python
# Por rol (RECOMENDADO)
element = page.get_by_role("button", name="Guardar")

# Por texto
element = page.get_by_text("Editar")

# Por placeholder
element = page.get_by_placeholder("Buscar...")

# Por CSS selector
element = page.locator("#username")
element = page.locator(".btn-primary")

# Combinados
element = page.locator("tr:has-text('1234567890')").locator(".btn-edit")
```

Para encontrar los selectores correctos:
1. Ejecuta con `headless=False` para ver el navegador
2. Usa `playwright codegen http://10.250.3.66:8080/savia` para generar selectores automáticamente
3. O inspecciona elementos manualmente en tu navegador

## 🚀 Uso

### Ejecutar la aplicación

```bash
python user_manager_app.py
```

### Flujo de trabajo

1. **Cargar imagen**
   - Clic en "📂 Seleccionar Imagen"
   - Selecciona una imagen con datos de usuario

2. **Extraer datos con OCR**
   - Clic en "🔍 Extraer Datos (OCR)"
   - Espera a que se procese
   - Verifica y edita los datos si es necesario

3. **Consultar en base de datos** (opcional)
   - Clic en "🔎 Consultar BD"
   - Verifica si el usuario existe

4. **Ejecutar acción**
   - Selecciona la acción: Cambiar Rol, Desactivar Usuario
   - Clic en "▶️ Ejecutar Acción"
   - Confirma la operación

5. **Revisar logs**
   - El panel inferior muestra todas las operaciones realizadas

## 📁 Estructura del proyecto

```
.
├── user_manager_app.py      # Aplicación principal con interfaz gráfica
├── ocr_processor.py          # Módulo de procesamiento OCR
├── database_handler.py       # Módulo de conexión a MySQL
├── web_automation.py         # Módulo de automatización web con Selenium
├── requirements.txt          # Dependencias de Python
├── database_setup.sql        # Script SQL para crear BD
├── .env.example              # Ejemplo de configuración
├── .env                      # Configuración (NO SUBIR A GIT)
└── README.md                 # Este archivo
```

## 🎨 Capturas de pantalla

La interfaz incluye:
- **Panel izquierdo:** Carga de imagen y vista previa
- **Panel derecho superior:** Datos extraídos (editables)
- **Panel derecho medio:** Selector de acciones
- **Panel derecho inferior:** Log de actividad en tiempo real

## 🔧 Personalización

### Mejorar precisión del OCR

Edita `ocr_processor.py` método `preprocess_image()`:
```python
# Ajustar umbralización
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY, 11, 2)

# Cambiar configuración de Tesseract
custom_config = r'--oem 3 --psm 6 -l spa'  # Cambiar PSM según tu caso
```

Modos PSM comunes:
- `6`: Asumir bloque uniforme de texto
- `3`: Orientación y script automático
- `11`: Texto disperso

### Agregar nuevos campos

1. Edita `user_manager_app.py` y agrega el campo en `fields`:
```python
fields = [
    # ... campos existentes ...
    ("Teléfono:", "telefono"),
]
```

2. Edita `ocr_processor.py` y agrega método de extracción:
```python
def _extract_phone(self, text):
    pattern = r'\b(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else ''
```

## 🐛 Solución de problemas

### Error: "Tesseract not found"
**Solución:** Agrega Tesseract al PATH o especifica la ruta en `ocr_processor.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Error: "Can't connect to MySQL server"
**Solución:** 
- Verifica que MySQL esté corriendo
- Revisa credenciales en `.env`
- Verifica firewall y permisos

### Error: "ChromeDriver version mismatch"
**Solución:**
```bash
pip install --upgrade webdriver-manager
```

### OCR no extrae correctamente los datos
**Soluciones:**
- Usa imágenes de alta calidad (300+ DPI)
- Asegúrate de que el texto esté horizontal
- Ajusta preprocesamiento en `ocr_processor.py`
- Prueba con diferentes valores de PSM en Tesseract

### La automatización web falla
**Soluciones:**
- Verifica que los selectores sean correctos
- Revisa que la plataforma no haya cambiado su estructura
- Prueba con `headless=False` para ver qué está pasando
- Aumenta los tiempos de espera

## 📊 Formato de imagen recomendado

Para mejores resultados con OCR, las imágenes deben:
- ✅ Estar en formato PNG o JPG
- ✅ Tener buena resolución (mínimo 300 DPI)
- ✅ Tener buen contraste entre texto y fondo
- ✅ Estar bien iluminadas sin sombras
- ✅ Tener texto horizontal (no rotado)
- ❌ Evitar imágenes borrosas o pixeladas
- ❌ Evitar texto muy pequeño (<12pt)

## 🔒 Seguridad

⚠️ **IMPORTANTE:**
- **NUNCA** subas el archivo `.env` a repositorios públicos
- Usa contraseñas fuertes para la base de datos
- Limita los permisos del usuario de base de datos (solo SELECT)
- Considera encriptar las credenciales en producción
- Usa conexiones SSL/TLS para la base de datos en producción

## 📝 Notas adicionales

- La base de datos es **solo lectura** desde Python (por seguridad)
- Todos los cambios se hacen a través de la automatización web
- Los logs se guardan solo en la interfaz (considera agregar persistencia)
- Puedes ejecutar en modo headless para producción

## 🤝 Contribuir

Si encuentras bugs o tienes sugerencias:
1. Documenta el problema claramente
2. Incluye pasos para reproducirlo
3. Propón una solución si es posible

## 📄 Licencia

Este proyecto es de código abierto. Úsalo y modifícalo según tus necesidades.

## ✨ Próximas mejoras sugeridas

- [ ] Soporte para múltiples imágenes en batch
- [ ] Exportar logs a archivo CSV
- [ ] Integración con API en lugar de automatización web
- [ ] Validación de datos más robusta
- [ ] Confirmación 2FA para la plataforma
- [ ] Dashboard con estadísticas
- [ ] Notificaciones por email
- [ ] Modo oscuro en la interfaz

---

**¿Necesitas ayuda?** Revisa la sección de solución de problemas o consulta la documentación de cada módulo.
