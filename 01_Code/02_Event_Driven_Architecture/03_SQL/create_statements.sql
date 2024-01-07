/*
Script: SQL Create Statements

Description: SQL file that simulates the data model of our grocery stores.

EDEM. Master Data Analytics 2023/2024
Weekday Group Professor: Miguel Moratilla
Weekend Group Professor: Javi Briones
*/

CREATE TABLE customers (
    customer_id UUID PRIMARY KEY,
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    store_id VARCHAR(255)
);

CREATE table products (
    product_id CHAR(6) PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10, 2)
);

CREATE TABLE purchases (
    purchase_id CHAR(10) PRIMARY KEY,
    customer_id UUID,
    purchase_date TIMESTAMP,
    total_amount DECIMAL(10, 2),
    payment_method VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE purchasedetails (
    purchase_detail_id SERIAL PRIMARY KEY,
    purchase_id CHAR(10),
    product_id CHAR(6),
    quantity INT,
    FOREIGN KEY (purchase_id) REFERENCES Purchases(purchase_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);