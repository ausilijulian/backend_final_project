CREATE DATABASE IF NOT EXISTS db_final_project2;
USE db_final_project2;

-- Crear la tabla Usuario
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Crear la tabla Cliente
CREATE TABLE IF NOT EXISTS client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    dni VARCHAR(20) NOT NULL,
    id_user INT,
    deleted BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_user) REFERENCES users(id)
);

-- Crear la tabla Producto_Servicio
CREATE TABLE IF NOT EXISTS product_service (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stock INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    img VARCHAR(255),
    type VARCHAR(10) NOT NULL,
    id_user INT,
    deleted BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_user) REFERENCES users(id)
);

-- Crear la tabla Receipt
CREATE TABLE IF NOT EXISTS receipt (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    code VARCHAR(255) NOT NULL,
    id_client INT,
    id_user INT,
    deleted BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_client) REFERENCES client(id),
    FOREIGN KEY (id_user) REFERENCES users(id)
);

-- Crear la tabla Detalle_Factura
CREATE TABLE IF NOT EXISTS receipt_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_receipt INT,
    id_product_service INT,
    quantity INT,
    unit_price DECIMAL(10, 2),
    FOREIGN KEY (id_receipt) REFERENCES receipt(id),
    FOREIGN KEY (id_product_service) REFERENCES product_service(id)
);