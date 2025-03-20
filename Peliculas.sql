CREATE DATABASE IF NOT EXISTS POPFILM;

CREATE TABLE peliculas (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    sinopsis VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL, 
    precio DECIMAL(9,2) NOT NULL,
    portada TEXT
    
);
INSERT INTO peliculas(nombre, sinopsis, categoria, portada, precio)
VALUES ('Ejemplo', 'Sinopsis de prueba', 'Comedia', 'PEPE', 19.99);

CREATE TABLE usuarios(
	usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    contrasena VARCHAR(255) NOT NULL,
    perfil VARCHAR(100) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    fechaUltimoAcceso DATE,
    fechaBloqueo DATE,
    numeroAccesosErroneo INTEGER,
    debeCambiarClave BOOLEAN
);



