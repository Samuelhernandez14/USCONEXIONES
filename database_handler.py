"""
Módulo para manejar conexiones y consultas a la base de datos SAVIA
MODO SOLO LECTURA - Adaptado para tabla gn_usuarios
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DatabaseHandler:
    def __init__(self):
        """Inicializar handler de base de datos SAVIA"""
        self.connection = None
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'system_savia'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci'
        }
        
        # Tabla de usuarios en SAVIA
        self.tabla_usuarios = 'gn_usuarios'
    
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
    
    def _convert_bit_to_bool(self, bit_value):
        """Convertir bit(1) a booleano"""
        if bit_value is None:
            return None
        if isinstance(bit_value, (bytes, bytearray)):
            return bit_value != b'\x00'
        return bool(bit_value)
    
    def _map_savia_user_to_standard(self, savia_user):
        """
        Mapear usuario de SAVIA al formato estándar del sistema
        
        Mapeo:
        - documento → numero_documento
        - mae_tipo_documento_codigo → tipo_documento
        - nombre → nombre_completo
        - correo_electronico → email
        - mae_cargo_valor → rol
        - mae_area_valor → area
        - activo (bit) → estado (texto)
        """
        if not savia_user:
            return None
        
        # Convertir activo de bit a booleano
        activo = self._convert_bit_to_bool(savia_user.get('activo'))
        
        return {
            'id': savia_user.get('id'),
            'tipo_documento': savia_user.get('mae_tipo_documento_codigo', ''),
            'numero_documento': savia_user.get('documento', ''),
            'nombre_completo': savia_user.get('nombre', ''),
            'email': savia_user.get('correo_electronico', ''),
            'usuario': savia_user.get('usuario', ''),
            'rol': savia_user.get('mae_cargo_valor', 'Sin cargo'),
            'area': savia_user.get('mae_area_valor', 'Sin área'),
            'estado': 'activo' if activo else 'inactivo',
            'fecha_creacion': savia_user.get('fecha_hora_crea'),
            'fecha_modificacion': savia_user.get('fecha_hora_modifica'),
            # Campos adicionales de SAVIA
            'telefono': savia_user.get('telefono'),
            'celular': savia_user.get('celular'),
            'empresa_id': savia_user.get('gn_empresas_id'),
            'grupo_id': savia_user.get('au_grupos_id'),
            'bloqueado': self._convert_bit_to_bool(savia_user.get('bloqueado')),
            'fecha_ultimo_ingreso': savia_user.get('fecha_ultimo_ingreso')
        }
    
    def get_user_by_document(self, numero_documento):
        """
        Buscar usuario por número de documento
        """
        query = f"""
            SELECT 
                id,
                gn_empresas_id,
                au_grupos_id,
                nombre,
                usuario,
                correo_electronico,
                mae_tipo_documento_id,
                mae_tipo_documento_codigo,
                mae_tipo_documento_valor,
                documento,
                mae_area_id,
                mae_area_codigo,
                mae_area_valor,
                mae_cargo_id,
                mae_cargo_codigo,
                mae_cargo_valor,
                telefono,
                celular,
                activo,
                bloqueado,
                fecha_ultimo_ingreso,
                fecha_hora_crea,
                fecha_hora_modifica
            FROM {self.tabla_usuarios}
            WHERE documento = %s
            LIMIT 1
        """
        
        results = self.execute_query(query, (numero_documento,))
        
        if results:
            return self._map_savia_user_to_standard(results[0])
        return None
    
    def get_user_by_email(self, email):
        """
        Buscar usuario por email
        """
        query = f"""
            SELECT 
                id,
                gn_empresas_id,
                au_grupos_id,
                nombre,
                usuario,
                correo_electronico,
                mae_tipo_documento_codigo,
                documento,
                mae_area_valor,
                mae_cargo_valor,
                activo,
                bloqueado,
                fecha_hora_crea,
                fecha_hora_modifica
            FROM {self.tabla_usuarios}
            WHERE correo_electronico = %s
            LIMIT 1
        """
        
        results = self.execute_query(query, (email,))
        
        if results:
            return self._map_savia_user_to_standard(results[0])
        return None
    
    def get_user_by_username(self, username):
        """
        Buscar usuario por nombre de usuario
        """
        query = f"""
            SELECT 
                id,
                nombre,
                usuario,
                correo_electronico,
                mae_tipo_documento_codigo,
                documento,
                mae_area_valor,
                mae_cargo_valor,
                activo,
                bloqueado,
                fecha_hora_crea,
                fecha_hora_modifica
            FROM {self.tabla_usuarios}
            WHERE usuario = %s
            LIMIT 1
        """
        
        results = self.execute_query(query, (username,))
        
        if results:
            return self._map_savia_user_to_standard(results[0])
        return None
    
    def search_users(self, search_term):
        """
        Buscar usuarios por nombre, email, documento o usuario
        """
        query = f"""
            SELECT 
                id,
                nombre,
                usuario,
                correo_electronico,
                mae_tipo_documento_codigo,
                documento,
                mae_area_valor,
                mae_cargo_valor,
                activo
            FROM {self.tabla_usuarios}
            WHERE 
                nombre LIKE %s
                OR correo_electronico LIKE %s
                OR documento LIKE %s
                OR usuario LIKE %s
            ORDER BY nombre
            LIMIT 50
        """
        
        search_pattern = f"%{search_term}%"
        results = self.execute_query(query, (search_pattern, search_pattern, search_pattern, search_pattern))
        
        return [self._map_savia_user_to_standard(user) for user in results]
    
    def get_users_by_role(self, rol):
        """
        Obtener usuarios por cargo (rol)
        """
        query = f"""
            SELECT 
                id,
                nombre,
                usuario,
                correo_electronico,
                documento,
                mae_area_valor,
                mae_cargo_valor,
                activo
            FROM {self.tabla_usuarios}
            WHERE mae_cargo_valor = %s
            ORDER BY nombre
        """
        
        results = self.execute_query(query, (rol,))
        return [self._map_savia_user_to_standard(user) for user in results]
    
    def get_users_by_area(self, area):
        """
        Obtener usuarios por área
        """
        query = f"""
            SELECT 
                id,
                nombre,
                usuario,
                correo_electronico,
                documento,
                mae_area_valor,
                mae_cargo_valor,
                activo
            FROM {self.tabla_usuarios}
            WHERE mae_area_valor = %s
            ORDER BY nombre
        """
        
        results = self.execute_query(query, (area,))
        return [self._map_savia_user_to_standard(user) for user in results]
    
    def get_active_users(self):
        """
        Obtener todos los usuarios activos
        """
        query = f"""
            SELECT 
                id,
                nombre,
                usuario,
                correo_electronico,
                mae_tipo_documento_codigo,
                documento,
                mae_area_valor,
                mae_cargo_valor
            FROM {self.tabla_usuarios}
            WHERE activo = 1
            ORDER BY nombre
        """
        
        results = self.execute_query(query)
        return [self._map_savia_user_to_standard(user) for user in results]
    
    def get_inactive_users(self):
        """
        Obtener todos los usuarios inactivos
        """
        query = f"""
            SELECT 
                id,
                nombre,
                usuario,
                correo_electronico,
                documento,
                mae_area_valor,
                mae_cargo_valor,
                fecha_hora_modifica
            FROM {self.tabla_usuarios}
            WHERE activo = 0
            ORDER BY fecha_hora_modifica DESC
        """
        
        results = self.execute_query(query)
        return [self._map_savia_user_to_standard(user) for user in results]
    
    def check_user_exists(self, numero_documento=None, email=None, username=None):
        """
        Verificar si existe un usuario por documento, email o usuario
        """
        if numero_documento:
            user = self.get_user_by_document(numero_documento)
            return user is not None
        
        if email:
            user = self.get_user_by_email(email)
            return user is not None
        
        if username:
            user = self.get_user_by_username(username)
            return user is not None
        
        return False
    
    def get_user_status(self, numero_documento):
        """
        Obtener solo el estado de un usuario
        """
        query = f"""
            SELECT activo
            FROM {self.tabla_usuarios}
            WHERE documento = %s
            LIMIT 1
        """
        
        results = self.execute_query(query, (numero_documento,))
        
        if results:
            activo = self._convert_bit_to_bool(results[0]['activo'])
            return 'activo' if activo else 'inactivo'
        return None
    
    def get_statistics(self):
        """
        Obtener estadísticas generales de usuarios
        """
        query = f"""
            SELECT 
                COUNT(*) as total_usuarios,
                SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as usuarios_activos,
                SUM(CASE WHEN activo = 0 THEN 1 ELSE 0 END) as usuarios_inactivos,
                COUNT(DISTINCT mae_cargo_valor) as total_cargos,
                COUNT(DISTINCT mae_area_valor) as total_areas
            FROM {self.tabla_usuarios}
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
    print("=== Test de DatabaseHandler para SAVIA ===\n")
    
    db = DatabaseHandler()
    
    print("Configuración de conexión:")
    print(f"Host: {db.config['host']}")
    print(f"Puerto: {db.config['port']}")
    print(f"Base de datos: {db.config['database']}")
    print(f"Usuario: {db.config['user']}")
    print(f"Tabla: {db.tabla_usuarios}")
    
    try:
        # Obtener estadísticas
        print("\n" + "="*60)
        print("ESTADÍSTICAS DE USUARIOS")
        print("="*60)
        
        stats = db.get_statistics()
        if stats:
            print(f"\nTotal de usuarios: {stats.get('total_usuarios', 0)}")
            print(f"Usuarios activos: {stats.get('usuarios_activos', 0)}")
            print(f"Usuarios inactivos: {stats.get('usuarios_inactivos', 0)}")
            print(f"Total de cargos: {stats.get('total_cargos', 0)}")
            print(f"Total de áreas: {stats.get('total_areas', 0)}")
        
        # Buscar usuario de ejemplo
        print("\n" + "="*60)
        print("BÚSQUEDA DE USUARIO DE EJEMPLO")
        print("="*60)
        
        # Obtener primer usuario activo
        users = db.get_active_users()
        if users:
            print(f"\nTotal de usuarios activos: {len(users)}")
            print("\nPrimer usuario activo:")
            user = users[0]
            print(f"  Nombre: {user.get('nombre_completo')}")
            print(f"  Usuario: {user.get('usuario')}")
            print(f"  Documento: {user.get('tipo_documento')} {user.get('numero_documento')}")
            print(f"  Email: {user.get('email')}")
            print(f"  Cargo: {user.get('rol')}")
            print(f"  Área: {user.get('area')}")
            print(f"  Estado: {user.get('estado')}")
        
        print("\n✅ Conexión exitosa y consultas funcionando")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nVerifica:")
        print("  • Archivo .env configurado correctamente")
        print("  • Conexión al servidor 10.250.5.35")
        print("  • Permisos de lectura en system_savia")