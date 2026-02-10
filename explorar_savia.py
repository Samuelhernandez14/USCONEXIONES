"""
Script para explorar la estructura de la base de datos SAVIA
Y encontrar la tabla de usuarios
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def explorar_savia():
    """Explorar base de datos SAVIA"""
    
    load_dotenv()
    
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'database': os.getenv('DB_NAME', 'system_savia'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
    }
    
    print("="*70)
    print("  EXPLORADOR DE BASE DE DATOS SAVIA")
    print("="*70)
    print(f"\nConectando a: {config['host']} -> {config['database']}")
    print(f"Usuario: {config['user']}")
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # 1. Listar todas las tablas
        print("\n" + "="*70)
        print("  TABLAS DISPONIBLES")
        print("="*70)
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\nTotal de tablas: {len(tables)}\n")
        
        # Buscar tablas relacionadas con usuarios
        user_tables = []
        
        for i, table in enumerate(tables, 1):
            table_name = table[0]
            print(f"{i:3}. {table_name}")
            
            # Identificar tablas de usuarios
            if any(keyword in table_name.lower() for keyword in ['user', 'usuario', 'person', 'persona', 'empleado', 'employee']):
                user_tables.append(table_name)
        
        # 2. Analizar tablas de usuarios encontradas
        if user_tables:
            print("\n" + "="*70)
            print("  TABLAS QUE PODRÍAN CONTENER USUARIOS")
            print("="*70)
            
            for table_name in user_tables:
                print(f"\n📋 Tabla: {table_name}")
                print("-"*70)
                
                # Obtener estructura
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                
                print("\nColumnas:")
                for col in columns:
                    print(f"  • {col[0]:<30} {col[1]:<20} {col[2]:<10}")
                
                # Contar registros
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"\nTotal de registros: {count}")
                    
                    # Mostrar primeros 3 registros
                    if count > 0:
                        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                        sample = cursor.fetchall()
                        
                        print("\nEjemplo de datos (primeros 3 registros):")
                        column_names = [col[0] for col in columns]
                        
                        for row in sample:
                            print("\n  Registro:")
                            for col_name, value in zip(column_names, row):
                                print(f"    {col_name}: {value}")
                    
                except Error as e:
                    print(f"  ⚠️ No se pueden ver los datos: {e}")
        
        else:
            print("\n⚠️ No se encontraron tablas obvias de usuarios")
            print("\nBuscando en todas las tablas...")
            
            # Analizar las primeras 10 tablas
            print("\n" + "="*70)
            print("  ESTRUCTURA DE LAS PRIMERAS 10 TABLAS")
            print("="*70)
            
            for table in tables[:10]:
                table_name = table[0]
                print(f"\n📋 {table_name}")
                print("-"*70)
                
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                
                # Buscar columnas interesantes
                interesting_cols = []
                for col in columns:
                    col_name = col[0].lower()
                    if any(keyword in col_name for keyword in ['doc', 'nombre', 'name', 'email', 'user', 'rol', 'perfil', 'cedula']):
                        interesting_cols.append(col[0])
                
                if interesting_cols:
                    print(f"  Columnas interesantes: {', '.join(interesting_cols)}")
                
                print(f"  Total columnas: {len(columns)}")
        
        # 3. Resumen y recomendaciones
        print("\n" + "="*70)
        print("  RESUMEN Y RECOMENDACIONES")
        print("="*70)
        
        if user_tables:
            print(f"\n✅ Encontradas {len(user_tables)} tabla(s) de usuarios:\n")
            for table in user_tables:
                print(f"   • {table}")
            
            print("\n📝 PRÓXIMO PASO:")
            print(f"\nElige la tabla principal de usuarios y envíame:")
            print(f"1. El nombre de la tabla")
            print(f"2. La estructura completa (DESCRIBE nombre_tabla)")
            print(f"\nPara eso, ejecuta:")
            print(f"   DESCRIBE {user_tables[0]};")
        else:
            print("\n⚠️ No se encontraron tablas obvias de usuarios")
            print("\nPor favor revisa manualmente:")
            print("   SHOW TABLES;")
            print("   DESCRIBE nombre_de_tabla_sospechosa;")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*70)
        
    except Error as e:
        print(f"\n❌ Error: {e}")
        print("\nVerifica:")
        print("  • Credenciales en .env")
        print("  • Conexión al servidor 10.250.5.35")
        print("  • Permisos de lectura en system_savia")

if __name__ == "__main__":
    explorar_savia()
    input("\nPresiona Enter para salir...")
