"""
Script de prueba para verificar la instalación correcta del sistema
Ejecutar: python test_installation.py
"""

import sys
import subprocess

def print_header(text):
    """Imprimir encabezado formateado"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Verificar versión de Python"""
    print_header("1. Verificando versión de Python")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Versión de Python compatible")
        return True
    else:
        print("❌ Se requiere Python 3.8 o superior")
        return False

def check_dependencies():
    """Verificar instalación de dependencias"""
    print_header("2. Verificando dependencias")
    
    dependencies = {
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'pytesseract': 'pytesseract',
        'mysql.connector': 'mysql-connector-python',
        'playwright.sync_api': 'playwright',
        'dotenv': 'python-dotenv'
    }
    
    all_ok = True
    
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {package:<30} instalado")
        except ImportError:
            print(f"❌ {package:<30} NO instalado")
            all_ok = False
    
    return all_ok

def check_playwright_browsers():
    """Verificar que los navegadores de Playwright estén instalados"""
    print_header("2b. Verificando navegadores de Playwright")
    
    try:
        from playwright.sync_api import sync_playwright
        
        print("✅ Playwright instalado")
        print("\nIntentando verificar navegadores...")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                browser.close()
                print("✅ Chromium instalado y funcional")
                return True
        except Exception as e:
            print(f"⚠️  Chromium no disponible: {str(e)}")
            print("\n   Solución: Ejecuta 'playwright install chromium'")
            return False
            
    except ImportError:
        print("❌ Playwright no está instalado")
        return False

def check_tesseract():
    """Verificar instalación de Tesseract OCR"""
    print_header("3. Verificando Tesseract OCR")
    
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract {version} instalado")
        return True
    except Exception as e:
        print(f"❌ Tesseract no encontrado o no configurado")
        print(f"   Error: {str(e)}")
        print("\n   Solución:")
        print("   - Windows: Descargar de https://github.com/UB-Mannheim/tesseract/wiki")
        print("   - Linux: sudo apt install tesseract-ocr")
        print("   - macOS: brew install tesseract")
        print("\n   Si ya está instalado, configura la ruta en ocr_processor.py:")
        print("   pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'")
        return False

def check_env_file():
    """Verificar archivo .env"""
    print_header("4. Verificando archivo de configuración (.env)")
    
    import os
    
    if os.path.exists('.env'):
        print("✅ Archivo .env existe")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
            'PLATFORM_URL', 'PLATFORM_USER', 'PLATFORM_PASSWORD'
        ]
        
        missing = []
        for var in required_vars:
            value = os.getenv(var)
            if not value or 'tu_' in value or 'your_' in value:
                missing.append(var)
        
        if missing:
            print(f"⚠️  Variables sin configurar: {', '.join(missing)}")
            print("   Edita el archivo .env con tus credenciales reales")
            return False
        else:
            print("✅ Todas las variables configuradas")
            return True
    else:
        print("❌ Archivo .env no encontrado")
        print("   Copia .env.example a .env y configura tus credenciales")
        return False

def check_database():
    """Verificar conexión a la base de datos"""
    print_header("5. Verificando conexión a MySQL")
    
    try:
        from database_handler import DatabaseHandler
        from dotenv import load_dotenv
        load_dotenv()
        
        db = DatabaseHandler()
        db.connect()
        print("✅ Conexión a MySQL exitosa")
        
        # Verificar tabla usuarios
        result = db.execute_query("SHOW TABLES LIKE 'usuarios'")
        if result:
            print("✅ Tabla 'usuarios' existe")
            
            # Contar usuarios
            count = db.execute_query("SELECT COUNT(*) as total FROM usuarios")
            total = count[0]['total'] if count else 0
            print(f"   📊 Total de usuarios en BD: {total}")
        else:
            print("⚠️  Tabla 'usuarios' no existe")
            print("   Ejecuta: mysql -u root -p < database_setup.sql")
        
        db.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Error en conexión a MySQL: {str(e)}")
        print("\n   Verifica:")
        print("   - MySQL está corriendo")
        print("   - Credenciales en .env son correctas")
        print("   - Base de datos 'usuarios_db' fue creada")
        return False

def check_modules():
    """Verificar que los módulos personalizados se importen correctamente"""
    print_header("6. Verificando módulos del proyecto")
    
    modules = [
        ('user_manager_app', 'Aplicación principal'),
        ('ocr_processor', 'Procesador OCR'),
        ('database_handler', 'Handler de BD'),
        ('web_automation', 'Automatización web')
    ]
    
    all_ok = True
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {description:<25} OK")
        except Exception as e:
            print(f"❌ {description:<25} Error: {str(e)}")
            all_ok = False
    
    return all_ok

def print_summary(results):
    """Imprimir resumen de resultados"""
    print_header("RESUMEN")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\nPruebas pasadas: {passed}/{total}")
    print(f"Pruebas fallidas: {failed}/{total}")
    
    if failed == 0:
        print("\n✅ ¡Todo listo! Puedes ejecutar la aplicación:")
        print("   python user_manager_app.py")
    else:
        print("\n⚠️  Hay problemas por resolver:")
        for test, passed in results.items():
            if not passed:
                print(f"   ❌ {test}")
        print("\nRevisa la documentación en README.md para solucionarlos")

def main():
    """Función principal"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║    Sistema de Gestión de Usuarios - Test de Instalación   ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    results = {}
    
    results['Python'] = check_python_version()
    results['Dependencias'] = check_dependencies()
    results['Navegadores Playwright'] = check_playwright_browsers()
    results['Tesseract'] = check_tesseract()
    results['Configuración'] = check_env_file()
    results['Base de datos'] = check_database()
    results['Módulos'] = check_modules()
    
    print_summary(results)

if __name__ == "__main__":
    main()