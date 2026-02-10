"""
Módulo para manejar conexiones y consultas a la base de datos MySQL
Solo consultas - NO se permite modificar datos desde aquí
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DatabaseHandler:
    def __init__(self):
        """Inicializar handler de base de datos"""
        self.connection = None
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'usuarios_db'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci'
        }
    
    def connect(self):
        """Establecer conexión con la base de datos"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
                if self.connection.is_connected():
                    return True
            return True
        except Error as e:
            raise Exception(f"Error al conectar a MySQL: {str(e)}")
    
    def disconnect(self):
        """Cerrar conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """
        Ejecutar consulta SELECT (solo lectura)
        """
        try:
            self.connect()
            cursor = self.connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            cursor.close()
            
            return results
        
        except Error as e:
            raise Exception(f"Error en consulta: {str(e)}")
    
    def get_user_by_document(self, numero_documento):
        """
        Buscar usuario por número de documento
        """
        query = """
            SELECT 
                id,
                tipo_documento,
                numero_documento,
                nombre_completo,
                email,
                rol,
                area,
                estado,
                fecha_creacion,
                fecha_modificacion
            FROM usuarios
            WHERE numero_documento = %s
            LIMIT 1
        """
        
        results = self.execute_query(query, (numero_documento,))
        
        if results:
            return results[0]
        return None
    
    def get_user_by_email(self, email):
        """
        Buscar usuario por email
        """
        query = """
            SELECT 
                id,
                tipo_documento,
                numero_documento,
                nombre_completo,
                email,
                rol,
                area,
                estado,
                fecha_creacion,
                fecha_modificacion
            FROM usuarios
            WHERE email = %s
            LIMIT 1
        """
        
        results = self.execute_query(query, (email,))
        
        if results:
            return results[0]
        return None
    
    def search_users(self, search_term):
        """
        Buscar usuarios por nombre, email o documento
        """
        query = """
            SELECT 
                id,
                tipo_documento,
                numero_documento,
                nombre_completo,
                email,
                rol,
                area,
                estado
            FROM usuarios
            WHERE 
                nombre_completo LIKE %s
                OR email LIKE %s
                OR numero_documento LIKE %s
            ORDER BY nombre_completo
            LIMIT 50
        """
        
        search_pattern = f"%{search_term}%"
        results = self.execute_query(query, (search_pattern, search_pattern, search_pattern))
        
        return results
    
    def get_users_by_role(self, rol):
        """
        Obtener usuarios por rol
        """
        query = """
            SELECT 
                id,
                numero_documento,
                nombre_completo,
                email,
                area,
                estado
            FROM usuarios
            WHERE rol = %s
            ORDER BY nombre_completo
        """
        
        return self.execute_query(query, (rol,))
    
    def get_users_by_area(self, area):
        """
        Obtener usuarios por área
        """
        query = """
            SELECT 
                id,
                numero_documento,
                nombre_completo,
                email,
                rol,
                estado
            FROM usuarios
            WHERE area = %s
            ORDER BY nombre_completo
        """
        
        return self.execute_query(query, (area,))
    
    def get_active_users(self):
        """
        Obtener todos los usuarios activos
        """
        query = """
            SELECT 
                id,
                tipo_documento,
                numero_documento,
                nombre_completo,
                email,
                rol,
                area
            FROM usuarios
            WHERE estado = 'activo'
            ORDER BY nombre_completo
        """
        
        return self.execute_query(query)
    
    def get_inactive_users(self):
        """
        Obtener todos los usuarios inactivos
        """
        query = """
            SELECT 
                id,
                tipo_documento,
                numero_documento,
                nombre_completo,
                email,
                rol,
                area,
                fecha_modificacion
            FROM usuarios
            WHERE estado = 'inactivo'
            ORDER BY fecha_modificacion DESC
        """
        
        return self.execute_query(query)
    
    def check_user_exists(self, numero_documento=None, email=None):
        """
        Verificar si existe un usuario por documento o email
        """
        if numero_documento:
            user = self.get_user_by_document(numero_documento)
            return user is not None
        
        if email:
            user = self.get_user_by_email(email)
            return user is not None
        
        return False
    
    def get_user_status(self, numero_documento):
        """
        Obtener solo el estado de un usuario
        """
        query = """
            SELECT estado
            FROM usuarios
            WHERE numero_documento = %s
            LIMIT 1
        """
        
        results = self.execute_query(query, (numero_documento,))
        
        if results:
            return results[0]['estado']
        return None
    
    def get_statistics(self):
        """
        Obtener estadísticas generales de usuarios
        """
        query = """
            SELECT 
                COUNT(*) as total_usuarios,
                SUM(CASE WHEN estado = 'activo' THEN 1 ELSE 0 END) as usuarios_activos,
                SUM(CASE WHEN estado = 'inactivo' THEN 1 ELSE 0 END) as usuarios_inactivos,
                COUNT(DISTINCT rol) as total_roles,
                COUNT(DISTINCT area) as total_areas
            FROM usuarios
        """
        
        results = self.execute_query(query)
        
        if results:
            return results[0]
        return None
    
    def __del__(self):
        """Destructor - cerrar conexión al eliminar objeto"""
        self.disconnect()


# Script de prueba
if __name__ == "__main__":
    print("=== Test de DatabaseHandler ===\n")
    
    db = DatabaseHandler()
    
    print("Configuración de conexión:")
    print(f"Host: {db.config['host']}")
    print(f"Puerto: {db.config['port']}")
    print(f"Base de datos: {db.config['database']}")
    print(f"Usuario: {db.config['user']}")
    print("\nNOTA: Asegúrate de configurar las variables en archivo .env")
    
    # Ejemplo de uso (descomentar cuando tengas la BD configurada)
    """
    try:
        # Buscar usuario
        user = db.get_user_by_document("1234567890")
        if user:
            print("\nUsuario encontrado:")
            for key, value in user.items():
                print(f"  {key}: {value}")
        else:
            print("\nUsuario no encontrado")
        
        # Obtener estadísticas
        stats = db.get_statistics()
        if stats:
            print("\nEstadísticas:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
    
    except Exception as e:
        print(f"\nError: {str(e)}")
    """
