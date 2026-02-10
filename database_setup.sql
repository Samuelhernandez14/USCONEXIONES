-- Script SQL para crear la base de datos y tabla de usuarios
-- Ejecutar en MySQL/MariaDB

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS usuarios_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE usuarios_db;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(10) NOT NULL COMMENT 'CC, CE, TI, PA, etc.',
    numero_documento VARCHAR(20) NOT NULL UNIQUE,
    nombre_completo VARCHAR(200) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    rol VARCHAR(50) NOT NULL COMMENT 'Administrador, Usuario, Operador, etc.',
    area VARCHAR(100) DEFAULT NULL COMMENT 'Área o departamento',
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_numero_documento (numero_documento),
    INDEX idx_email (email),
    INDEX idx_estado (estado),
    INDEX idx_rol (rol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar datos de ejemplo
INSERT INTO usuarios (tipo_documento, numero_documento, nombre_completo, email, rol, area, estado) VALUES
('CC', '1234567890', 'Juan Carlos Pérez Rodríguez', 'juan.perez@empresa.com', 'Administrador', 'Tecnología', 'activo'),
('CC', '9876543210', 'María Fernanda López García', 'maria.lopez@empresa.com', 'Usuario', 'Recursos Humanos', 'activo'),
('CE', '1122334455', 'Carlos Eduardo Martínez Silva', 'carlos.martinez@empresa.com', 'Operador', 'Operaciones', 'activo'),
('TI', '1011121314', 'Ana Isabel Ramírez Torres', 'ana.ramirez@empresa.com', 'Supervisor', 'Ventas', 'inactivo'),
('CC', '5566778899', 'Pedro Antonio González Ruiz', 'pedro.gonzalez@empresa.com', 'Analista', 'Finanzas', 'activo');

-- Crear tabla de log de cambios (opcional pero recomendado)
CREATE TABLE IF NOT EXISTS log_cambios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    numero_documento VARCHAR(20) NOT NULL,
    accion VARCHAR(50) NOT NULL COMMENT 'cambio_rol, desactivar, activar, etc.',
    campo_modificado VARCHAR(50) DEFAULT NULL,
    valor_anterior VARCHAR(200) DEFAULT NULL,
    valor_nuevo VARCHAR(200) DEFAULT NULL,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    realizado_por VARCHAR(100) DEFAULT 'Sistema OCR',
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_numero_documento (numero_documento),
    INDEX idx_fecha_cambio (fecha_cambio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Consultas útiles para verificación

-- Ver todos los usuarios
-- SELECT * FROM usuarios;

-- Ver usuarios activos
-- SELECT * FROM usuarios WHERE estado = 'activo';

-- Ver usuarios por rol
-- SELECT * FROM usuarios WHERE rol = 'Administrador';

-- Ver historial de cambios
-- SELECT * FROM log_cambios ORDER BY fecha_cambio DESC LIMIT 10;
