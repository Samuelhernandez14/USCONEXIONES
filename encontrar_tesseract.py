"""
Script para encontrar la instalación de Tesseract en Windows
"""

import os
import subprocess
import sys

def find_tesseract_windows():
    """Buscar Tesseract en ubicaciones comunes de Windows"""
    
    print("🔍 Buscando Tesseract OCR en tu sistema...\n")
    
    # Ubicaciones comunes en Windows
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{username}\AppData\Local\Tesseract-OCR\tesseract.exe",
    ]
    
    # Agregar path con username actual
    username = os.environ.get('USERNAME', '')
    if username:
        common_paths.append(
            rf"C:\Users\{username}\AppData\Local\Tesseract-OCR\tesseract.exe"
        )
    
    found_paths = []
    
    # Buscar en paths comunes
    print("Buscando en ubicaciones comunes...")
    for path in common_paths:
        if os.path.exists(path):
            found_paths.append(path)
            print(f"  ✅ Encontrado: {path}")
    
    # Intentar ejecutar desde PATH
    print("\nVerificando PATH del sistema...")
    try:
        result = subprocess.run(
            ['tesseract', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("  ✅ Tesseract está en el PATH del sistema")
            print(f"  Versión: {result.stdout.split()[1] if result.stdout else 'desconocida'}")
            
            # Intentar obtener la ruta completa
            try:
                where_result = subprocess.run(
                    ['where', 'tesseract'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if where_result.returncode == 0:
                    path = where_result.stdout.strip().split('\n')[0]
                    if path not in found_paths:
                        found_paths.append(path)
                        print(f"  Ubicación: {path}")
            except:
                pass
                
    except FileNotFoundError:
        print("  ❌ Tesseract no está en el PATH")
    except subprocess.TimeoutExpired:
        print("  ⚠️  Timeout al verificar PATH")
    except Exception as e:
        print(f"  ⚠️  Error: {str(e)}")
    
    # Mostrar resultados
    print("\n" + "="*60)
    
    if found_paths:
        print(f"✅ Tesseract encontrado en {len(found_paths)} ubicación(es):\n")
        for i, path in enumerate(found_paths, 1):
            print(f"{i}. {path}")
        
        print("\n" + "="*60)
        print("📝 CONFIGURACIÓN REQUERIDA")
        print("="*60)
        print("\nEdita el archivo ocr_processor.py:")
        print("Busca la línea que dice:")
        print('  TESSERACT_PATH = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"')
        print("\nCámbiala por:")
        print(f'  TESSERACT_PATH = r"{found_paths[0]}"')
        
    else:
        print("❌ Tesseract NO encontrado en tu sistema\n")
        print("📥 SOLUCIÓN: Instalar Tesseract")
        print("="*60)
        print("\n1. Descarga Tesseract desde:")
        print("   https://github.com/UB-Mannheim/tesseract/wiki")
        print("\n2. Ejecuta el instalador")
        print("\n3. Durante la instalación:")
        print("   ✓ Marca la opción 'Add Tesseract to PATH'")
        print("   ✓ Anota la carpeta de instalación")
        print("\n4. Después de instalar, ejecuta este script nuevamente:")
        print("   python encontrar_tesseract.py")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    find_tesseract_windows()
    
    input("\nPresiona Enter para salir...")
