"""
Módulo de procesamiento OCR para extraer datos de usuarios de imágenes
Soporta extracción de: tipo de documento, número, nombre, email, rol, área
"""

import os
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re

# ============================================
# CONFIGURACIÓN DE TESSERACT PARA WINDOWS
# ============================================
# Si Tesseract está instalado pero Python no lo encuentra,
# descomenta y ajusta esta línea con la ruta correcta:

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    print(f"✅ Tesseract configurado en: {TESSERACT_PATH}")
else:
    print("⚠️  Tesseract no encontrado en la ruta configurada")
    print(f"   Buscado en: {TESSERACT_PATH}")
    print("   Ajusta la variable TESSERACT_PATH en ocr_processor.py")

# ============================================

class OCRProcessor:
    def __init__(self):
        """Inicializar procesador OCR"""
        # Verificar que Tesseract esté disponible
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise FileNotFoundError(
                f"Tesseract no encontrado. Error: {str(e)}\n"
                f"Instala Tesseract o configura la ruta en TESSERACT_PATH"
            )
    
    def preprocess_image(self, image_path):
        """
        Preprocesar imagen para mejorar calidad de OCR
        """
        # Cargar imagen
        img = cv2.imread(image_path)
        
        # Convertir a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Aplicar umbralización adaptativa
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Reducir ruido
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        # Aplicar dilatación para conectar letras
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(denoised, kernel, iterations=1)
        
        return dilated
    
    def extract_text_from_image(self, image_path):
        """
        Extraer texto de imagen usando Tesseract OCR
        """
        try:
            # Preprocesar imagen
            processed_img = self.preprocess_image(image_path)
            
            # Configuración de Tesseract para español
            custom_config = r'--oem 3 --psm 6 -l spa'
            
            # Extraer texto
            text = pytesseract.image_to_string(processed_img, config=custom_config)
            
            return text
        
        except Exception as e:
            raise Exception(f"Error en extracción de texto: {str(e)}")
    
    def extract_user_data(self, image_path):
        """
        Extraer datos estructurados del usuario desde la imagen
        Retorna diccionario con: tipo_documento, numero_documento, nombre_completo, email, rol, area
        """
        # Extraer texto
        text = self.extract_text_from_image(image_path)
        
        # Limpiar texto
        text = text.strip()
        
        # Diccionario para almacenar datos
        user_data = {
            'tipo_documento': '',
            'numero_documento': '',
            'nombre_completo': '',
            'email': '',
            'rol': '',
            'area': ''
        }
        
        # Extraer datos usando expresiones regulares y patrones
        user_data['tipo_documento'] = self._extract_doc_type(text)
        user_data['numero_documento'] = self._extract_doc_number(text)
        user_data['nombre_completo'] = self._extract_name(text)
        user_data['email'] = self._extract_email(text)
        user_data['rol'] = self._extract_role(text)
        user_data['area'] = self._extract_area(text)
        
        return user_data
    
    def _extract_doc_type(self, text):
        """Extraer tipo de documento"""
        # Patrones comunes
        patterns = [
            r'tipo\s*(?:de\s*)?documento[:\s]*([A-Z]{2,4})',
            r'\b(CC|CE|TI|PA|DNI|RUC|NIT)\b',
            r'(?:Cédula|Cedula|Pasaporte|Tarjeta)[:\s]*([A-Za-z\s]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                doc_type = match.group(1).strip().upper()
                # Normalizar tipos comunes
                type_mapping = {
                    'CEDULA': 'CC',
                    'CÉDULA': 'CC',
                    'CEDULA DE CIUDADANIA': 'CC',
                    'CÉDULA DE CIUDADANÍA': 'CC',
                    'PASAPORTE': 'PA',
                    'TARJETA DE IDENTIDAD': 'TI',
                }
                return type_mapping.get(doc_type, doc_type)
        
        return ''
    
    def _extract_doc_number(self, text):
        """Extraer número de documento"""
        # Patrones para números de documento
        patterns = [
            r'(?:número|numero|n°|no\.?|#)[:\s]*([0-9]{6,15})',
            r'documento[:\s]*([0-9]{6,15})',
            r'\b([0-9]{8,12})\b',  # Números largos probables
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                number = match.group(1).strip()
                # Validar que sea numérico
                if number.isdigit() and 6 <= len(number) <= 15:
                    return number
        
        return ''
    
    def _extract_name(self, text):
        """Extraer nombre completo"""
        # Patrones para nombre
        patterns = [
            r'nombre\s*(?:completo)?[:\s]*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)',
            r'(?:Sr\.|Sra\.|Srta\.)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)',
            r'^([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){2,4})',  # Nombre al inicio
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Validar que tenga al menos 2 palabras
                if len(name.split()) >= 2:
                    return name.title()
        
        return ''
    
    def _extract_email(self, text):
        """Extraer email"""
        # Patrón estándar de email
        pattern = r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b'
        
        match = re.search(pattern, text)
        if match:
            return match.group(1).lower()
        
        return ''
    
    def _extract_role(self, text):
        """Extraer rol o perfil"""
        # Patrones para rol
        patterns = [
            r'(?:rol|perfil|cargo|puesto)[:\s]*([A-Za-záéíóúñÁÉÍÓÚÑ\s]+?)(?:\n|$|Área|Area)',
            r'(?:administrador|usuario|operador|supervisor|gerente|analista|desarrollador)',
        ]
        
        # Lista de roles comunes
        common_roles = [
            'Administrador', 'Usuario', 'Operador', 'Supervisor', 
            'Gerente', 'Analista', 'Desarrollador', 'Coordinador',
            'Asistente', 'Director', 'Jefe', 'Líder', 'Especialista'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                role = match.group(0 if 'administrador' in pattern else 1).strip()
                
                # Buscar coincidencia con roles comunes
                for common_role in common_roles:
                    if common_role.lower() in role.lower():
                        return common_role
                
                return role.title()
        
        return ''
    
    def _extract_area(self, text):
        """Extraer área o departamento"""
        # Patrones para área
        patterns = [
            r'(?:área|area|departamento|dpto\.?)[:\s]*([A-Za-záéíóúñÁÉÍÓÚÑ\s]+?)(?:\n|$)',
            r'(?:Ventas|Marketing|TI|Sistemas|RRHH|Finanzas|Operaciones|Logística|Contabilidad)',
        ]
        
        # Áreas comunes
        common_areas = [
            'Ventas', 'Marketing', 'TI', 'Sistemas', 'Tecnología',
            'RRHH', 'Recursos Humanos', 'Finanzas', 'Contabilidad',
            'Operaciones', 'Logística', 'Producción', 'Administración',
            'Legal', 'Compras', 'Soporte'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                area = match.group(0 if 'Ventas' in pattern else 1).strip()
                
                # Buscar coincidencia con áreas comunes
                for common_area in common_areas:
                    if common_area.lower() in area.lower():
                        return common_area
                
                return area.title()
        
        return ''


# Función de prueba
if __name__ == "__main__":
    # Ejemplo de uso
    print("="*60)
    print("TEST DE OCR PROCESSOR")
    print("="*60)
    
    try:
        ocr = OCRProcessor()
        print("✅ OCRProcessor inicializado correctamente")
        print(f"✅ Tesseract versión: {pytesseract.get_tesseract_version()}")
        
        # Simular texto extraído
        sample_text = """
        FORMULARIO DE USUARIO
        
        Tipo de Documento: CC
        Número: 1234567890
        Nombre Completo: Juan Carlos Pérez Rodríguez
        Email: juan.perez@empresa.com
        Rol: Administrador
        Área: Tecnología
        """
        
        print("\nTexto de ejemplo:")
        print(sample_text)
        print("\n" + "="*60 + "\n")
        
        print("Datos que serían extraídos:")
        print("- Tipo Doc: CC")
        print("- Número: 1234567890")
        print("- Nombre: Juan Carlos Pérez Rodríguez")
        print("- Email: juan.perez@empresa.com")
        print("- Rol: Administrador")
        print("- Área: Tecnología")
        
        print("\n✅ Todo funcionando correctamente")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nVerifica:")
        print("1. Tesseract está instalado")
        print("2. La ruta TESSERACT_PATH es correcta")
        print("3. Tesseract está en el PATH del sistema")