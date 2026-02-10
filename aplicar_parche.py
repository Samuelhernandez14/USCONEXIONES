"""
Parche temporal para pytesseract en Python 3.14
Reemplaza find_loader que fue eliminado en Python 3.14
"""

import os
import sys
import sites

def encontrar_pytesseract():
    """Encontrar la ubicación de pytesseract"""
    for path in site.getsitepackages():
        pytesseract_path = os.path.join(path, 'pytesseract', 'pytesseract.py')
        if os.path.exists(pytesseract_path):
            return pytesseract_path
    return None

def aplicar_parche():
    """Aplicar parche al archivo pytesseract.py"""
    
    pytesseract_file = encontrar_pytesseract()
    
    if not pytesseract_file:
        print("❌ No se encontró pytesseract instalado")
        return False
    
    print(f"📍 Archivo encontrado: {pytesseract_file}")
    
    # Leer contenido
    try:
        with open(pytesseract_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return False
    
    # Verificar si ya está parcheado
    if 'PARCHE PYTHON 3.14' in content:
        print("✅ El archivo ya está parcheado")
        return True
    
    # Aplicar parche
    old_import = "from pkgutil import find_loader"
    new_import = """# PARCHE PYTHON 3.14 - Reemplazar find_loader
try:
    from pkgutil import find_loader
except ImportError:
    # Python 3.14+ no tiene find_loader
    from importlib.util import find_spec
    def find_loader(name):
        spec = find_spec(name)
        return spec.loader if spec else None"""
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        
        # Guardar con backup
        backup_file = pytesseract_file + '.backup'
        try:
            # Crear backup
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content.replace(new_import, old_import))
            
            # Guardar parcheado
            with open(pytesseract_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Parche aplicado correctamente")
            print(f"💾 Backup creado: {backup_file}")
            return True
            
        except PermissionError:
            print("❌ Error: No tienes permisos para modificar el archivo")
            print("   Ejecuta como Administrador (Windows) o con sudo (Linux/Mac)")
            return False
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
            return False
    else:
        print("⚠️  No se encontró el import a reemplazar")
        print("   Puede que pytesseract ya esté actualizado")
        return False

if __name__ == "__main__":
    print("="*70)
    print("  PARCHE PARA PYTESSERACT EN PYTHON 3.14")
    print("="*70)
    print()
    print("Este script modifica pytesseract para que funcione con Python 3.14")
    print()
    
    confirm = input("¿Continuar? (s/n): ").lower()
    
    if confirm == 's':
        print("\n🔧 Aplicando parche...\n")
        
        if aplicar_parche():
            print("\n✅ ¡Listo! Ahora puedes ejecutar la aplicación:")
            print("   python user_manager_app.py")
        else:
            print("\n❌ No se pudo aplicar el parche")
            print("\nPrueba estas alternativas:")
            print("1. Ejecuta este script como Administrador")
            print("2. O usa: python solucionar_python314.py")
    else:
        print("\nOperación cancelada")
    
    input("\nPresiona Enter para salir...")
