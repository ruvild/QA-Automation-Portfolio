DROP DATABASE IF EXISTS sql_practice;
CREATE DATABASE sql_practice;
USE sql_practice;

-- =========================
-- CUSTOMERS
-- =========================
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    signup_date DATE
);

INSERT INTO customers (first_name, last_name, email, city, signup_date) VALUES
('John', 'Doe', 'john@example.com', 'Amsterdam', '2023-01-10'),
('Jane', 'Smith', 'jane@example.com', 'Berlin', '2023-02-15'),
('Alice', 'Brown', 'alice@example.com', 'Paris', '2023-03-05'),
('Bob', 'White', 'bob@example.com', 'Madrid', '2023-04-20'),
('Charlie', 'Black', 'charlie@example.com', 'Amsterdam', '2023-05-12'),
('Diana', 'Green', 'diana@example.com', 'Rome', '2023-06-01');

-- =========================
-- CATEGORIES
-- =========================
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50)
);

INSERT INTO categories (category_name) VALUES
('Electronics'),
('Clothing'),
('Home'),
('Sports');

-- =========================
-- PRODUCTS
-- =========================
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100),
    category_id INT,
    price DECIMAL(10,2),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

INSERT INTO products (product_name, category_id, price) VALUES
('Laptop', 1, 1200.00),
('Headphones', 1, 150.00),
('T-Shirt', 2, 25.00),
('Jeans', 2, 60.00),
('Coffee Maker', 3, 80.00),
('Vacuum Cleaner', 3, 200.00),
('Football', 4, 30.00),
('Tennis Racket', 4, 120.00);

-- =========================
-- ORDERS
-- =========================
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO orders (customer_id, order_date, status) VALUES
(1, '2023-06-10', 'completed'),
(2, '2023-06-11', 'completed'),
(1, '2023-06-15', 'completed'),
(3, '2023-06-20', 'cancelled'),
(4, '2023-07-01', 'completed'),
(5, '2023-07-03', 'completed'),
(6, '2023-07-05', 'completed'),
(2, '2023-07-06', 'completed'),
(3, '2023-07-10', 'completed');

-- =========================
-- ORDER ITEMS
-- =========================
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 1200.00),
(1, 2, 2, 150.00),
(2, 3, 3, 25.00),
(2, 4, 1, 60.00),
(3, 5, 1, 80.00),
(3, 2, 1, 150.00),
(4, 1, 1, 1200.00),
(5, 6, 1, 200.00),
(6, 7, 2, 30.00),
(7, 8, 1, 120.00),
(8, 3, 2, 25.00),
(9, 1, 1, 1200.00);

-- =========================
-- PAYMENTS
-- =========================
CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    payment_date DATE,
    amount DECIMAL(10,2),
    method VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

INSERT INTO payments (order_id, payment_date, amount, method) VALUES
(1, '2023-06-10', 1500.00, 'credit_card'),
(2, '2023-06-11', 135.00, 'paypal'),
(3, '2023-06-15', 230.00, 'credit_card'),
(5, '2023-07-01', 200.00, 'debit_card'),
(6, '2023-07-03', 60.00, 'paypal'),
(7, '2023-07-05', 120.00, 'credit_card'),
(8, '2023-07-06', 50.00, 'credit_card'),
(9, '2023-07-10', 1200.00, 'paypal');