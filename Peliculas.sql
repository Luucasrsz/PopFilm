CREATE DATABASE IF NOT EXISTS POPFILM;

CREATE TABLE peliculas (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    sinopsis VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL, 
    portada VARCHAR(255)
);

CREATE TABLE usuarios (
    email VARCHAR(255) NOT NULL PRIMARY KEY,
    contrasena VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    logeado BOOLEAN DEFAULT false
);

INSERT INTO usuarios (email, contrasena, nombre, logeado) 
VALUES ('a', 'a', 'Lucas', FALSE);


