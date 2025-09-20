USE na_sales;

-- Drop tables if they exist to start fresh
DROP TABLE IF EXISTS ORDER_ITEMS;
DROP TABLE IF EXISTS ORDERS;
DROP TABLE IF EXISTS CUSTOMERS;

-- 1. Create the CUSTOMERS table
CREATE TABLE CUSTOMERS (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- 2. Create the ORDERS table with a foreign key to CUSTOMERS
CREATE TABLE ORDERS (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id)
);

-- 3. Create the ORDER_ITEMS table with a foreign key to ORDERS
CREATE TABLE ORDER_ITEMS (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
);

-- Insert data into CUSTOMERS
INSERT INTO CUSTOMERS (first_name, last_name, region) VALUES
('Jane', 'Doe', 'North America'),
('John', 'Smith', 'Europe'),
('Emily', 'Jones', 'North America'),
('Chris', 'Lee', 'Asia');

-- Insert data into ORDERS
INSERT INTO ORDERS (customer_id, order_date, status) VALUES
(1, '2023-08-15', 'Shipped'),
(2, '2023-09-20', 'Processing'),
(1, '2023-10-01', 'Delivered'),
(3, '2023-11-05', 'Shipped'),
(4, '2024-01-10', 'Delivered');

-- Insert data into ORDER_ITEMS
INSERT INTO ORDER_ITEMS (order_id, product_name, quantity, price_per_unit) VALUES
(1, 'Laptop', 1, 1200.00),
(1, 'Mouse', 1, 25.00),
(2, 'Keyboard', 2, 75.00),
(3, 'Monitor', 1, 300.00),
(4, 'Headphones', 1, 150.00),
(5, 'Webcam', 1, 50.00),
(5, 'Microphone', 1, 75.00);


-- Example of a join query: Find all orders for a specific customer
SELECT
    C.first_name,
    C.last_name,
    O.order_id,
    O.order_date
FROM
    CUSTOMERS AS C
JOIN
    ORDERS AS O ON C.customer_id = O.customer_id
WHERE
    C.first_name = 'Jane';

-- Example of a more complex join: Find all products ordered by customers in 'North America'
SELECT
    C.first_name,
    C.last_name,
    O.order_date,
    OI.product_name,
    OI.quantity,
    OI.price_per_unit
FROM
    CUSTOMERS AS C
JOIN
    ORDERS AS O ON C.customer_id = O.customer_id
JOIN
    ORDER_ITEMS AS OI ON O.order_id = OI.order_id
WHERE
    C.region = 'North America';
