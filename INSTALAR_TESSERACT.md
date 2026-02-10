# 🔧 Guía de Instalación de Tesseract OCR para Windows

## ¿Qué es Tesseract?
Tesseract es el motor OCR (reconocimiento óptico de caracteres) que permite extraer texto de imágenes. Es esencial para que este proyecto funcione.

---

## 📥 Paso 1: Descargar Tesseract

### Opción A: Instalador Oficial (Recomendado)

1. **Ir a la página de descargas:**
   ```
   https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Descargar el instalador más reciente:**
   - Busca: `tesseract-ocr-w64-setup-5.x.x.xxxxxxxx.exe`
   - Descarga la versión de 64 bits (w64)

### Opción B: Descarga Directa

Si el link anterior no funciona, usa este:
```
https://digi.bib.uni-mannheim.de/tesseract/
```

---

## 🛠️ Paso 2: Instalar Tesseract

1. **Ejecutar el instalador descargado**
   - Doble clic en `tesseract-ocr-w64-setup-x.x.x.exe`

2. **Durante la instalación:**

   **PASO IMPORTANTE 1:** Cuando aparezca "Select Components"
   ```
   ✅ Marca: Additional language data
   ✅ Marca: Spanish (spa)
   ```

   **PASO IMPORTANTE 2:** Cuando aparezca "Select Additional Tasks"
   ```
   ✅ MARCA ESTA OPCIÓN: "Add Tesseract to PATH"
   ```
   ⚠️ **¡MUY IMPORTANTE!** Si no marcas esto, Python no encontrará Tesseract

   **PASO 3:** Anota la carpeta de instalación
   ```
   Ubicación típica: C:\Program Files\Tesseract-OCR
   ```

3. **Completar la instalación**
   - Click en "Install"
   - Esperar a que termine
   - Click en "Finish"

---

## ✅ Paso 3: Verificar Instalación

### Método 1: Desde una nueva terminal

1. **Abrir una NUEVA ventana de PowerShell o CMD**
   ```
   IMPORTANTE: Debe ser una ventana nueva para que cargue el PATH
   ```

2. **Ejecutar:**
   ```bash
   tesseract --version
   ```

3. **Resultado esperado:**
   ```
   tesseract 5.x.x
   leptonica-1.x.x
   ...
   ```

   - ✅ Si ves esto → Tesseract está instalado correctamente
   - ❌ Si dice "no se reconoce" → Ve al Paso 4

### Método 2: Usar nuestro script

```bash
python encontrar_tesseract.py
```

Este script buscará Tesseract automáticamente y te dirá:
- Si está instalado
- Dónde está ubicado
- Qué configurar en el código

---

## 🔧 Paso 4: Configurar en el Proyecto

### Opción A: Si Tesseract está en PATH (recomendado)

Si el comando `tesseract --version` funcionó, NO necesitas hacer nada más.
El código lo encontrará automáticamente.

### Opción B: Si Tesseract NO está en PATH

1. **Encontrar la ubicación de Tesseract:**
   ```bash
   python encontrar_tesseract.py
   ```

2. **Editar `ocr_processor.py`:**

   Abre el archivo y busca esta línea (cerca de la línea 10):
   ```python
   TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

   Cámbiala por la ruta donde está instalado en TU computadora:
   ```python
   # Ejemplo 1: Instalación estándar
   TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   
   # Ejemplo 2: Instalación en Program Files (x86)
   TESSERACT_PATH = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
   
   # Ejemplo 3: Instalación personalizada
   TESSERACT_PATH = r"C:\Tesseract\tesseract.exe"
   ```

3. **Guardar el archivo**

---

## 🧪 Paso 5: Probar

### Test rápido del OCR:

```bash
python ocr_processor.py
```

**Resultado esperado:**
```
============================================================
TEST DE OCR PROCESSOR
============================================================
✅ Tesseract configurado en: C:\Program Files\Tesseract-OCR\tesseract.exe
✅ OCRProcessor inicializado correctamente
✅ Tesseract versión: 5.x.x
...
✅ Todo funcionando correctamente
```

### Test completo del sistema:

```bash
python test_installation.py
```

Busca esta sección:
```
============================================================
  3. Verificando Tesseract OCR
============================================================
✅ Tesseract 5.x.x instalado
```

---

## 🐛 Solución de Problemas

### Error: "tesseract is not installed or it's not in your PATH"

**Causa:** Python no encuentra Tesseract

**Soluciones:**

1. **Verificar instalación:**
   ```bash
   # Abrir una NUEVA terminal
   tesseract --version
   ```

2. **Si el comando funciona pero Python no lo encuentra:**
   - Configura la ruta manualmente en `ocr_processor.py`
   - Usa el script `encontrar_tesseract.py` para obtener la ruta exacta

3. **Si el comando NO funciona:**
   - Tesseract no está en el PATH
   - Agrega manualmente al PATH del sistema:
     ```
     Panel de Control → Sistema → Configuración avanzada del sistema
     → Variables de entorno → Path → Editar
     → Nuevo → C:\Program Files\Tesseract-OCR
     → Aceptar todo
     → REINICIAR la terminal
     ```

### Error: "FileNotFoundError: Tesseract no encontrado"

**Solución:**
1. Ejecuta `python encontrar_tesseract.py`
2. Anota la ruta que te muestre
3. Edita `ocr_processor.py` con esa ruta

### Error: "TesseractNotFoundError"

**Solución:**
```bash
# Reinstalar Tesseract
# 1. Desinstalar el actual (Panel de Control → Programas)
# 2. Reiniciar la computadora
# 3. Instalar nuevamente MARCANDO "Add to PATH"
```

---

## 📋 Checklist Final

Después de instalar, verifica:

- [ ] ✅ Tesseract instalado (con idioma español)
- [ ] ✅ Agregado al PATH del sistema
- [ ] ✅ Comando `tesseract --version` funciona en terminal nueva
- [ ] ✅ Script `encontrar_tesseract.py` lo encuentra
- [ ] ✅ Script `ocr_processor.py` lo inicializa correctamente
- [ ] ✅ Test completo `test_installation.py` pasa la prueba de Tesseract

---

## 🎯 Siguiente Paso

Una vez que Tesseract esté funcionando:

```bash
# Ejecutar test completo
python test_installation.py
```

Deberías ver:
```
============================================================
  3. Verificando Tesseract OCR
============================================================
✅ Tesseract 5.x.x instalado
```

---

## 🆘 Si Nada Funciona

1. **Desinstalar Tesseract:**
   - Panel de Control → Programas → Desinstalar

2. **Reiniciar la computadora**

3. **Reinstalar Tesseract:**
   - Descargar nuevamente
   - MARCAR "Add to PATH" durante instalación
   - MARCAR "Spanish language data"

4. **Abrir una NUEVA terminal**

5. **Probar:**
   ```bash
   tesseract --version
   python encontrar_tesseract.py
   ```

---

## 📞 Soporte

Si después de seguir todos estos pasos aún no funciona:

1. Ejecuta: `python encontrar_tesseract.py`
2. Toma captura del resultado
3. Ejecuta: `python test_installation.py`
4. Toma captura de la sección de Tesseract
5. Muéstrame ambas capturas para ayudarte

---

**¡Listo!** Con Tesseract instalado, tu sistema OCR estará funcional. 🎉
