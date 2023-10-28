
CREATE DATABASE IF NOT EXISTS db_final_project;
USE db_final_project;

-- Crear la tabla Usuario
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
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
    FOREIGN KEY (id_user) REFERENCES users(id)
);

-- Crear la tabla Producto_Servicio
CREATE TABLE IF NOT EXISTS product_service (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    img VARCHAR(255),
    type VARCHAR(10) NOT NULL,
    id_user INT,
    FOREIGN KEY (id_user) REFERENCES users(id)
);

-- Crear la tabla Receipt
CREATE TABLE IF NOT EXISTS receipt (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    id_client INT,
    id_user INT,
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


-- Insertar el primer cliente para el Usuario 1
INSERT INTO client (name, surname, email, dni, id_user) VALUES ('Cliente1', 'Apellido1', 'cliente1@email.com', '1234567890', 1);

-- Insertar el segundo cliente para el Usuario 1
INSERT INTO client (name, surname, email, dni, id_user) VALUES ('Cliente2', 'Apellido2', 'cliente2@email.com', '0987654321', 1);
Insertar Clientes para el Usuario 2:


-- Insertar el primer cliente para el Usuario 1
INSERT INTO client (name, surname, email, dni, id_user) VALUES ('Cliente1', 'Apellido1', 'cliente1@email.com', '1234567890', 1);

-- Insertar el segundo cliente para el Usuario 1
INSERT INTO client (name, surname, email, dni, id_user) VALUES ('Cliente2', 'Apellido2', 'cliente2@email.com', '0987654321', 1);


-- Insertar el primer cliente para el Usuario 2
INSERT INTO client (name, surname, email, dni, id_user) VALUES ('Cliente3', 'Apellido3', 'cliente3@email.com', '5555555555', 2);

-- Insertar el segundo cliente para el Usuario 2
INSERT INTO client (name, surname, email, dni, id_user) VALUES ('Cliente4', 'Apellido4', 'cliente4@email.com', '9999999999', 2);

-- Insertar productos y servicios para el Usuario 1
INSERT INTO product_service (stock, price, description, img, type, id_user)
VALUES
    (100, 29.99, 'Producto 1', 'producto1.jpg', 'Producto', 1),
    (50, 49.99, 'Producto 2', 'producto2.jpg', 'Producto', 1),
    (10, 79.99, 'Servicio 1', 'servicio1.jpg', 'Servicio', 1);

-- Insertar productos y servicios para el Usuario 2
INSERT INTO product_service (stock, price, description, img, type, id_user)
VALUES
    (75, 39.99, 'Producto 3', 'producto3.jpg', 'Producto', 2),
    (30, 59.99, 'Producto 4', 'producto4.jpg', 'Producto', 2),
    (5, 99.99, 'Servicio 2', 'servicio2.jpg', 'Servicio', 2);

-- Insertar facturas para el Usuario 1 y Cliente 1
INSERT INTO receipt (date, id_client, id_user)
VALUES
    ('2023-10-01', 1, 1),
    ('2023-10-15', 1, 1);

-- Insertar facturas para el Usuario 2 y Cliente 3
INSERT INTO receipt (date, id_client, id_user)
VALUES
    ('2023-10-05', 3, 2),
    ('2023-10-20', 3, 2);

-- Insertar detalles de factura para la Factura 1 (Usuario 1, Cliente 1)
INSERT INTO receipt_detail (id_receipt, id_product_service, quantity, unit_price)
VALUES
    (1, 1, 2, 29.99),
    (1, 2, 1, 49.99),
    (1, 3, 1, 79.99);

-- Insertar detalles de factura para la Factura 2 (Usuario 1, Cliente 1)
INSERT INTO receipt_detail (id_receipt, id_product_service, quantity, unit_price)
VALUES
    (2, 1, 3, 29.99),
    (2, 3, 2, 79.99);