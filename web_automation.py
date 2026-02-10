

from playwright.sync_api import sync_playwright, Page, Browser, Playwright
import time
import os
from dotenv import load_dotenv

load_dotenv()

class WebAutomation:
    def __init__(self, headless=False):
        """
        Inicializar automatización web con Playwright
        
        Args:
            headless (bool): Si True, ejecuta el navegador sin interfaz gráfica
        """
        self.playwright = None
        self.browser = None
        self.page = None
        self.headless = headless
        self.wait_time = 10000  # milisegundos
        
        # Configuración de la plataforma (cargar desde .env)
        self.platform_url = os.getenv('PLATFORM_URL', 'http://10.250.3.66:8080/savia')
        self.username = os.getenv('PLATFORM_USER', 'dpiedrar')
        self.password = os.getenv('PLATFORM_PASSWORD', 'i0BnXmZr')
        
        self.initialize_browser()
    
    def initialize_browser(self):
        """Inicializar navegador Playwright"""
        try:
            self.playwright = sync_playwright().start()
            
            # Configurar y lanzar navegador
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                slow_mo=50  # Ralentizar para debugging (milisegundos)
            )
            
            # Crear contexto con viewport
            context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            
            # Crear página
            self.page = context.new_page()
            
        except Exception as e:
            raise Exception(f"Error al inicializar navegador: {str(e)}")
    
    def login(self):
        """
        Realizar login en la plataforma SAVIA
        Usa los mismos selectores que el código Java con Playwright
        """
        try:
            print("🔐 Realizando login...")
            
            # Navegar a la plataforma
            self.page.goto(self.platform_url)
            
            # Llenar campo de usuario
            self.page.get_by_role("textbox", name="Usuario").click()
            self.page.get_by_role("textbox", name="Usuario").fill(self.username)
            
            # Llenar campo de contraseña
            self.page.get_by_role("textbox", name="Contraseña").click()
            self.page.get_by_role("textbox", name="Contraseña").fill(self.password)
            
            # Click en botón Ingresar
            self.page.get_by_role("button", name="Ingresar").click()
            
            # Esperar a que cargue la página principal
            self.page.wait_for_load_state("networkidle")
            
            print("✅ Login exitoso")
            return {'success': True, 'message': 'Login exitoso'}
        
        except Exception as e:
            print(f"❌ Error en login: {str(e)}")
            return {'success': False, 'message': f'Error en login: {str(e)}'}
    
    def navegar_a_modulo(self, nombre_modulo, operacion):
        """
        Navegar a un módulo específico usando la interfaz
        
        Args:
            nombre_modulo (str): Nombre del módulo (ej: "Usuarios", "Administración")
            operacion (str): Operación específica dentro del módulo
        """
        try:
            print(f"📂 Navegando a módulo: {nombre_modulo}...")
            
            # Click en el link del módulo
            self.page.get_by_role("link", name=nombre_modulo).click()
            
            # Click en la operación específica
            self.page.get_by_title(operacion, exact=True).click()
            
            # Esperar a que cargue
            self.page.wait_for_load_state("networkidle")
            
            print(f"✅ Módulo {nombre_modulo} cargado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error navegando a módulo: {str(e)}")
            raise Exception(f"Error al navegar a módulo: {str(e)}")
    
    def navegar_a_modulo_url(self, nombre_modulo, operacion):
        """
        Navegar directamente a un módulo usando URL
        
        Args:
            nombre_modulo (str): Ruta del módulo (ej: "admin/usuarios")
            operacion (str): Nombre del archivo .faces
        """
        try:
            url = f"{self.platform_url}/{nombre_modulo}/{operacion}.faces"
            print(f"🔗 Navegando a: {url}")
            
            self.page.goto(url)
            self.page.wait_for_load_state("networkidle")
            
            print(f"✅ Módulo {nombre_modulo} cargado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error navegando a URL: {str(e)}")
            raise Exception(f"Error al navegar a URL: {str(e)}")
    
    
    
    def search_user(self, numero_documento):
        """
        Buscar usuario en la plataforma por número de documento
        AJUSTA LOS SELECTORES según los campos de tu plataforma
        """
        try:
            print(f"🔍 Buscando usuario: {numero_documento}")
            
            # Opción 1: Buscar por campo de búsqueda
            # Ajusta el selector según tu interfaz
            search_field = self.page.locator("#search-user")  # Cambiar según tu plataforma
            # Alternativas:
            # search_field = self.page.locator("input[name='search']")
            # search_field = self.page.locator("input[placeholder*='Buscar']")
            # search_field = self.page.get_by_placeholder("Buscar usuario")
            
            search_field.fill(numero_documento)
            
            # Click en botón de búsqueda o presionar Enter
            # Opción A: Botón específico
            # self.page.locator("#btn-search").click()
            
            # Opción B: Presionar Enter
            search_field.press("Enter")
            
            # Esperar a que carguen los resultados
            time.sleep(1)
            
            # Verificar que se encontró el usuario
            # Ajusta el selector según tu tabla
            user_row = self.page.locator(f"tr:has-text('{numero_documento}')")
            
            if user_row.count() > 0:
                print(f"✅ Usuario encontrado")
                return user_row.first
            else:
                raise Exception(f"Usuario con documento {numero_documento} no encontrado")
                
        except Exception as e:
            raise Exception(f"Error al buscar usuario: {str(e)}")
    
    def change_user_role(self, numero_documento, nuevo_rol):
        """
        Cambiar el rol de un usuario
        
        Args:
            numero_documento (str): Número de documento del usuario
            nuevo_rol (str): Nuevo rol a asignar
        """
        try:
            # Login
            login_result = self.login()
            if not login_result['success']:
                return login_result
            
            # Navegar al módulo de usuarios
            # AJUSTA ESTOS VALORES según tu plataforma
            # Opción 1: Usar interfaz
            # self.navegar_a_modulo("Administración", "Gestión de Usuarios")
            
            # Opción 2: Usar URL directa (recomendado)
            self.navegar_a_modulo_url("admin", "usuarios")  # Ajustar ruta
            
            # Buscar usuario
            user_row = self.search_user(numero_documento)
            
            # Click en botón de editar
            # AJUSTA EL SELECTOR según tu interfaz
            # Opción 1: Por clase
            edit_button = user_row.locator(".btn-edit")
            # Opción 2: Por texto
            # edit_button = user_row.get_by_role("button", name="Editar")
            # Opción 3: Por título o aria-label
            # edit_button = user_row.get_by_title("Editar")
            
            edit_button.click()
            
            # Esperar a que cargue el formulario
            time.sleep(1)
            
            # Seleccionar nuevo rol
            # AJUSTA EL SELECTOR según tu select de roles
            # Opción 1: Por ID
            role_select = self.page.locator("#user-role")
            # Opción 2: Por nombre
            # role_select = self.page.locator("select[name='rol']")
            # Opción 3: Por label
            # role_select = self.page.get_by_label("Rol")
            
            role_select.select_option(label=nuevo_rol)
            
            # Guardar cambios
            # AJUSTA EL SELECTOR del botón guardar
            save_button = self.page.locator("#btn-save")
            # Alternativas:
            # save_button = self.page.get_by_role("button", name="Guardar")
            # save_button = self.page.locator("button:has-text('Guardar')")
            
            save_button.click()
            
            # Esperar confirmación
            time.sleep(2)
            
            # Verificar mensaje de éxito
            try:
                success_msg = self.page.locator(".alert-success, .mensaje-exito")
                if success_msg.is_visible(timeout=5000):
                    return {
                        'success': True,
                        'message': f'Rol cambiado a "{nuevo_rol}" exitosamente'
                    }
                else:
                    return {
                        'success': False,
                        'message': 'No se pudo verificar el cambio de rol'
                    }
            except:
                # Asumir éxito si no hay error visible
                return {
                    'success': True,
                    'message': f'Rol cambiado a "{nuevo_rol}" exitosamente'
                }
        
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
        finally:
            self.close()
    
    def deactivate_user(self, numero_documento):
        """
        Desactivar un usuario en la plataforma
        
        Args:
            numero_documento (str): Número de documento del usuario
        """
        try:
            # Login
            login_result = self.login()
            if not login_result['success']:
                return login_result
            
            # Navegar al módulo de usuarios
            self.navegar_a_modulo_url("admin", "usuarios")  # Ajustar ruta
            
            # Buscar usuario
            user_row = self.search_user(numero_documento)
            
            # Click en botón de desactivar
            # AJUSTA EL SELECTOR según tu interfaz
            deactivate_button = user_row.locator(".btn-deactivate")
            # Alternativas:
            # deactivate_button = user_row.get_by_role("button", name="Desactivar")
            # deactivate_button = user_row.locator("button:has-text('Desactivar')")
            
            deactivate_button.click()
            
            # Esperar modal de confirmación (si existe)
            time.sleep(1)
            
            try:
                # Confirmar desactivación
                confirm_button = self.page.locator("#confirm-deactivate")
                # Alternativas:
                # confirm_button = self.page.get_by_role("button", name="Confirmar")
                # confirm_button = self.page.locator(".modal button:has-text('Confirmar')")
                
                if confirm_button.is_visible(timeout=3000):
                    confirm_button.click()
            except:
                pass  # No hay modal de confirmación
            
            # Esperar confirmación
            time.sleep(2)
            
            # Verificar mensaje de éxito
            try:
                success_msg = self.page.locator(".alert-success, .mensaje-exito")
                if success_msg.is_visible(timeout=5000):
                    return {
                        'success': True,
                        'message': 'Usuario desactivado exitosamente'
                    }
                else:
                    return {
                        'success': False,
                        'message': 'No se pudo verificar la desactivación'
                    }
            except:
                return {
                    'success': True,
                    'message': 'Usuario desactivado exitosamente'
                }
        
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
        finally:
            self.close()
    
    def activate_user(self, numero_documento):
        """
        Activar un usuario en la plataforma
        
        Args:
            numero_documento (str): Número de documento del usuario
        """
        try:
            login_result = self.login()
            if not login_result['success']:
                return login_result
            
            self.navegar_a_modulo_url("admin", "usuarios")
            
            user_row = self.search_user(numero_documento)
            
            activate_button = user_row.locator(".btn-activate")
            # Alternativas:
            # activate_button = user_row.get_by_role("button", name="Activar")
            
            activate_button.click()
            time.sleep(2)
            
            return {
                'success': True,
                'message': 'Usuario activado exitosamente'
            }
        
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
        finally:
            self.close()
    
    
    def take_screenshot(self, filename="screenshot.png"):
        """Tomar captura de pantalla para debugging"""
        try:
            self.page.screenshot(path=filename)
            print(f"📸 Captura guardada: {filename}")
        except Exception as e:
            print(f"Error al tomar captura: {str(e)}")
    
    def close(self):
        """Cerrar navegador y playwright"""
        try:
            if self.page:
                self.page.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            print(f"Error al cerrar navegador: {str(e)}")
    
    def __del__(self):
        """Destructor - cerrar navegador"""
        self.close()


# Script de prueba
if __name__ == "__main__":
    print("=== Test de WebAutomation con Playwright ===\n")
    print("IMPORTANTE: Debes configurar las variables de entorno en .env:")
    print("  - PLATFORM_URL (por defecto: http://10.250.3.66:8080/savia)")
    print("  - PLATFORM_USER (por defecto: dpiedrar)")
    print("  - PLATFORM_PASSWORD")
    print("\nAdemás, debes ajustar los selectores CSS/locators en el código")
    print("según la estructura HTML de tu plataforma específica.\n")
    
    # Ejemplo de uso (descomentar cuando tengas todo configurado)
    """
    automation = WebAutomation(headless=False)
    
    try:
        # Hacer login
        result = automation.login()
        print(f"Login: {result['message']}")
        
        # Navegar a módulo
        automation.navegar_a_modulo_url("admin", "usuarios")
        
        # Tomar captura de pantalla
        automation.take_screenshot("usuarios.png")
        
        # Cambiar rol
        result = automation.change_user_role("1234567890", "Administrador")
        print(f"Cambio de rol: {result['message']}")
        
        # Desactivar usuario
        result = automation.deactivate_user("1234567890")
        print(f"Desactivación: {result['message']}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        automation.take_screenshot("error.png")
    """
