# 🎯 Guía de Configuración de Selectores - Plataforma SAVIA

## 📌 Información importante

Tu plataforma usa **Playwright** igual que tu código Java. Los selectores ya están adaptados para el login, pero necesitas configurar los selectores específicos para la gestión de usuarios.

## 🔐 Login (YA CONFIGURADO)

El login ya está funcionando con estos selectores de tu código Java:

```python
# Usuario
self.page.get_by_role("textbox", name="Usuario")

# Contraseña
self.page.get_by_role("textbox", name="Contraseña")

# Botón ingresar
self.page.get_by_role("button", name="Ingresar")
```

## 📂 Navegación a módulos

### Opción 1: Usar interfaz (como tu código Java)

```python
# Navegar al módulo de usuarios
automation.navegar_a_modulo("Administración", "Gestión de Usuarios")
```

### Opción 2: Usar URL directa (más rápido)

```python
# Ejemplo: http://10.250.3.66:8080/savia/admin/usuarios.faces
automation.navegar_a_modulo_url("admin", "usuarios")
```

**Necesitas identificar:**
- ¿Cuál es la ruta del módulo de usuarios? (ej: `admin`, `gestion`, `usuarios`)
- ¿Cuál es el nombre del archivo? (ej: `usuarios`, `gestionUsuarios`)

## 🔍 Cómo encontrar los selectores correctos

### Paso 1: Abrir DevTools en Playwright

Ejecuta tu aplicación con modo inspector:

```bash
# Opción 1: Modo inspector de Playwright
playwright codegen http://10.250.3.66:8080/savia

# Opción 2: Ejecutar con headless=False y usar DevTools
python web_automation.py
```

### Paso 2: Identificar elementos

En el Playwright Inspector, puedes:
1. Hacer hover sobre elementos
2. Ver el selector generado automáticamente
3. Copiar y pegar en tu código

### Paso 3: Tipos de selectores en Playwright

```python
# Por rol (RECOMENDADO - más estable)
page.get_by_role("button", name="Guardar")
page.get_by_role("textbox", name="Buscar")

# Por texto visible
page.get_by_text("Editar")
page.locator("button:has-text('Guardar')")

# Por placeholder
page.get_by_placeholder("Buscar usuario...")

# Por label
page.get_by_label("Nombre completo")

# Por título
page.get_by_title("Editar usuario")

# Por CSS selector
page.locator("#btn-save")
page.locator(".btn-primary")
page.locator("button.btn-edit")

# Por XPath (último recurso)
page.locator("xpath=//button[@id='save']")

# Combinados
page.locator("tr:has-text('1234567890')").locator(".btn-edit")
```

## ⚙️ Selectores que DEBES configurar

### 1. Campo de búsqueda de usuarios

Ubicación en código: `web_automation.py` → método `search_user()`

```python
# ACTUAL (línea ~155):
search_field = self.page.locator("#search-user")

# OPCIONES para reemplazar:
search_field = self.page.get_by_placeholder("Buscar")
search_field = self.page.locator("input[name='busqueda']")
search_field = self.page.locator("#campo-busqueda")
```

**Cómo encontrarlo:**
1. Inicia sesión manualmente en la plataforma
2. Ve a la gestión de usuarios
3. Inspecciona el campo de búsqueda
4. Copia el selector

### 2. Fila de usuario en tabla

Ubicación: `web_automation.py` → método `search_user()`

```python
# ACTUAL (línea ~170):
user_row = self.page.locator(f"tr:has-text('{numero_documento}')")

# Este selector probablemente funcione, pero verifica que:
# - La tabla muestre el número de documento
# - No haya múltiples filas con el mismo número
```

### 3. Botón de editar usuario

Ubicación: `web_automation.py` → método `change_user_role()`

```python
# ACTUAL (línea ~210):
edit_button = user_row.locator(".btn-edit")

# OPCIONES:
edit_button = user_row.get_by_role("button", name="Editar")
edit_button = user_row.get_by_title("Editar")
edit_button = user_row.locator("a[title='Editar']")
edit_button = user_row.locator("button:has-text('Editar')")
```

### 4. Select de rol

Ubicación: `web_automation.py` → método `change_user_role()`

```python
# ACTUAL (línea ~230):
role_select = self.page.locator("#user-role")

# OPCIONES:
role_select = self.page.get_by_label("Rol")
role_select = self.page.locator("select[name='rol']")
role_select = self.page.locator("#selectRol")
```

### 5. Botón guardar

Ubicación: `web_automation.py` → método `change_user_role()`

```python
# ACTUAL (línea ~240):
save_button = self.page.locator("#btn-save")

# OPCIONES:
save_button = self.page.get_by_role("button", name="Guardar")
save_button = self.page.locator("button:has-text('Guardar')")
save_button = self.page.locator(".btn-save")
```

### 6. Botón desactivar

Ubicación: `web_automation.py` → método `deactivate_user()`

```python
# ACTUAL (línea ~285):
deactivate_button = user_row.locator(".btn-deactivate")

# OPCIONES:
deactivate_button = user_row.get_by_role("button", name="Desactivar")
deactivate_button = user_row.get_by_title("Desactivar usuario")
deactivate_button = user_row.locator("button:has-text('Desactivar')")
```

## 📋 Checklist de configuración

- [ ] Identificar ruta del módulo de usuarios (para `navegar_a_modulo_url`)
- [ ] Selector del campo de búsqueda
- [ ] Selector del botón de búsqueda (o usar Enter)
- [ ] Selector de la fila del usuario
- [ ] Selector del botón "Editar"
- [ ] Selector del select de "Rol"
- [ ] Selector del botón "Guardar"
- [ ] Selector del botón "Desactivar"
- [ ] Selector del botón "Confirmar" (si existe modal)
- [ ] Selector del mensaje de éxito

## 🧪 Proceso de testing

### 1. Crear archivo de prueba

```python
# test_selectors.py
from web_automation import WebAutomation
import time

automation = WebAutomation(headless=False)

try:
    # Test 1: Login
    print("Test 1: Login...")
    result = automation.login()
    print(f"✅ Login: {result['message']}")
    time.sleep(2)
    
    # Test 2: Navegación
    print("\nTest 2: Navegación...")
    automation.navegar_a_modulo_url("admin", "usuarios")  # AJUSTAR RUTA
    print("✅ Navegación exitosa")
    time.sleep(2)
    
    # Test 3: Búsqueda
    print("\nTest 3: Búsqueda...")
    user_row = automation.search_user("1234567890")  # USAR DOCUMENTO REAL
    print("✅ Usuario encontrado")
    time.sleep(2)
    
    # Test 4: Screenshot
    automation.take_screenshot("test_usuarios.png")
    print("✅ Captura guardada")
    
    input("\nPresiona Enter para cerrar...")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    automation.take_screenshot("error.png")
    
finally:
    automation.close()
```

### 2. Ejecutar paso a paso

```bash
python test_selectors.py
```

Si falla, revisa:
1. La captura de pantalla `error.png`
2. El mensaje de error
3. Ajusta el selector y vuelve a intentar

## 💡 Tips importantes

### 1. Prioridad de selectores (de mejor a peor)

1. **Por rol** - `get_by_role()` - Más estable
2. **Por texto visible** - `get_by_text()` - Fácil de mantener
3. **Por label/placeholder** - `get_by_label()` - Semántico
4. **Por ID** - `#mi-id` - Único pero puede cambiar
5. **Por clase** - `.mi-clase` - Puede no ser único
6. **Por XPath** - Último recurso, muy frágil

### 2. Esperas inteligentes

Playwright espera automáticamente, pero si necesitas:

```python
# Esperar elemento visible
self.page.wait_for_selector(".mi-elemento", state="visible")

# Esperar elemento oculto
self.page.wait_for_selector(".modal", state="hidden")

# Esperar carga de red
self.page.wait_for_load_state("networkidle")
```

### 3. Debugging

```python
# Pausar ejecución
self.page.pause()

# Ver logs
self.page.on("console", lambda msg: print(f"Console: {msg.text}"))

# Tomar screenshot
self.page.screenshot(path="debug.png")
```

## 📞 ¿Necesitas ayuda?

Si algún selector no funciona:

1. Toma una captura con `automation.take_screenshot("problema.png")`
2. Inspecciona el elemento en Chrome DevTools
3. Prueba diferentes tipos de selectores
4. Usa `page.pause()` para debugging interactivo

---

**¡Listo!** Una vez ajustes estos selectores, el sistema estará completamente funcional.
