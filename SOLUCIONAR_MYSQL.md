# 🔧 Solución: Error de Permisos en MySQL

## ❌ Error Actual

```
Error al conectar a MySQL: 1044 (42000): Access denied for user 'shernanb'@'172.16.38.%' 
to database 'usuarios_db'
```

**Problema:** El usuario `shernanb` no tiene permisos para acceder a la base de datos `usuarios_db`.

---

## 🎯 Soluciones (Elige UNA)

### Solución A: Dar Permisos al Usuario Actual (Recomendado)

Esta es la solución más rápida si tienes acceso root.

#### Paso 1: Conectar como root

```bash
mysql -u root -p
```

Te pedirá la contraseña de root de MySQL.

#### Paso 2: Crear la BD y dar permisos

```sql
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS usuarios_db 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Dar TODOS los permisos a shernanb
GRANT ALL PRIVILEGES ON usuarios_db.* TO 'shernanb'@'172.16.38.%';
GRANT ALL PRIVILEGES ON usuarios_db.* TO 'shernanb'@'localhost';
GRANT ALL PRIVILEGES ON usuarios_db.* TO 'shernanb'@'%';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Salir
exit;
```

#### Paso 3: Crear las tablas

```bash
# Ejecutar el script completo
mysql -u root -p < setup_database_complete.sql
```

---

### Solución B: Usar Script Automático (Más Fácil)

Ya preparé un script SQL completo que hace todo automáticamente.

```bash
# Ejecutar como root
mysql -u root -p < setup_database_complete.sql
```

Este script:
- ✅ Crea la base de datos
- ✅ Crea las tablas (usuarios y log_cambios)
- ✅ Inserta datos de ejemplo
- ✅ Da permisos a shernanb
- ✅ Verifica que todo funcione

---

### Solución C: Cambiar de Usuario en .env

Si no tienes acceso root, usa tu usuario actual con una BD que sí tengas acceso.

#### Paso 1: Verificar qué bases de datos tienes acceso

```bash
mysql -u shernanb -p
```

Dentro de MySQL:
```sql
SHOW DATABASES;
```

#### Paso 2: Crear BD en una que tengas permisos

Si tienes acceso a crear bases de datos:

```sql
CREATE DATABASE usuarios_db;
USE usuarios_db;
SOURCE setup_database_complete.sql;
exit;
```

#### Paso 3: Actualizar .env

```env
DB_HOST=172.16.38.X  # La IP de tu servidor MySQL
DB_PORT=3306
DB_NAME=usuarios_db
DB_USER=shernanb
DB_PASSWORD=tu_password_aqui
```

---

### Solución D: Usar Usuario Root (Temporal)

⚠️ **No recomendado para producción, solo para pruebas**

#### Edita el archivo .env:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=usuarios_db
DB_USER=root
DB_PASSWORD=tu_password_de_root
```

#### Crea la base de datos:

```bash
mysql -u root -p < setup_database_complete.sql
```

---

## 🚀 Pasos Recomendados (MÉTODO RÁPIDO)

### 1. Ejecutar script como root

```bash
mysql -u root -p < setup_database_complete.sql
```

### 2. Actualizar archivo .env

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=usuarios_db
DB_USER=shernanb
DB_PASSWORD=TU_PASSWORD_DE_SHERNANB
```

### 3. Verificar conexión

```bash
python test_installation.py
```

Deberías ver:
```
============================================================
  5. Verificando conexión a MySQL
============================================================
✅ Conexión a MySQL exitosa
✅ Tabla 'usuarios' existe
   📊 Total de usuarios en BD: 5
```

---

## 🐛 Solución de Problemas

### Error: "Access denied for user 'root'"

**Problema:** No recuerdas la contraseña de root

**Solución:**
```bash
# Windows - Reiniciar MySQL sin autenticación
1. Detener servicio MySQL
2. Abrir CMD como Administrador
3. Ejecutar:
   mysqld --skip-grant-tables

4. En otra ventana:
   mysql -u root
   
5. Cambiar password:
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'nueva_password';
   FLUSH PRIVILEGES;
   exit;
   
6. Reiniciar MySQL normalmente
```

### Error: "Unknown database 'usuarios_db'"

**Solución:**
```sql
-- Conectar como root
mysql -u root -p

-- Crear base de datos
CREATE DATABASE usuarios_db;

-- Ejecutar script
SOURCE setup_database_complete.sql;
```

### Error: "Can't connect to MySQL server"

**Solución:**
```bash
# Verificar que MySQL esté corriendo

# Windows:
net start MySQL80

# O desde Servicios (services.msc):
Buscar "MySQL" → Clic derecho → Iniciar
```

### Error: "Host '172.16.38.X' is not allowed"

**Solución:**
```sql
-- Como root, dar permisos desde cualquier host
GRANT ALL PRIVILEGES ON usuarios_db.* TO 'shernanb'@'%' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
```

---

## 📋 Checklist

- [ ] MySQL está corriendo
- [ ] Tienes acceso root O permisos para crear BD
- [ ] Archivo .env tiene credenciales correctas
- [ ] Script SQL ejecutado exitosamente
- [ ] Permisos otorgados al usuario
- [ ] Test de conexión pasa

---

## 🧪 Comandos de Verificación

```bash
# 1. ¿MySQL está corriendo?
# Windows:
sc query MySQL80

# 2. ¿Puedo conectar?
mysql -u shernanb -p

# 3. ¿La BD existe?
mysql -u shernanb -p -e "SHOW DATABASES;"

# 4. ¿Tengo permisos?
mysql -u shernanb -p -e "SHOW GRANTS FOR CURRENT_USER;"

# 5. ¿Las tablas existen?
mysql -u shernanb -p usuarios_db -e "SHOW TABLES;"

# 6. ¿Test completo?
python test_installation.py
```

---

## 💡 Alternativa: MySQL Workbench

Si prefieres usar interfaz gráfica:

1. **Abrir MySQL Workbench**
2. **Conectar como root**
3. **Copiar y pegar** el contenido de `setup_database_complete.sql`
4. **Ejecutar** (ícono de rayo ⚡)
5. **Verificar** que se crearon las tablas

---

## 🎯 Siguiente Paso

Una vez solucionado MySQL:

```bash
python test_installation.py
```

Deberías ver:
```
Pruebas pasadas: 7/7
Pruebas fallidas: 0/7

✅ ¡Todo listo! Puedes ejecutar la aplicación:
   python user_manager_app.py
```

---

## 📞 Si Sigues Teniendo Problemas

Envíame el output de estos comandos:

```bash
# 1. Verificar conexión
mysql -u shernanb -p -e "SELECT USER(), CURRENT_USER();"

# 2. Ver bases de datos disponibles
mysql -u shernanb -p -e "SHOW DATABASES;"

# 3. Ver permisos actuales
mysql -u shernanb -p -e "SHOW GRANTS FOR 'shernanb'@'172.16.38.%';"

# 4. Test de Python
python test_installation.py
```
