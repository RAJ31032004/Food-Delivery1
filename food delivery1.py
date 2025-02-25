CREATE DATABASE IF NOT EXISTS food_delivery_system;
USE food_delivery_system;

-- Create Users table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- Create Restaurants table
CREATE TABLE IF NOT EXISTS Restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(50) NOT NULL,
    cuisine_type VARCHAR(50) NOT NULL,
    rating DECIMAL(3,2) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT true,
    opening_hours TIME NOT NULL,
    closing_hours TIME NOT NULL,
    INDEX idx_cuisine (cuisine_type),
    INDEX idx_rating (rating)
);

-- Create Menu_Items table
CREATE TABLE IF NOT EXISTS Menu_Items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    is_available BOOLEAN DEFAULT true,
    image_url VARCHAR(255),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
    INDEX idx_category (category),
    INDEX idx_restaurant (restaurant_id)
);

-- Create Delivery_Partners table
CREATE TABLE IF NOT EXISTS Delivery_Partners (
    partner_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(50) NOT NULL UNIQUE,
    vehicle_type VARCHAR(50) NOT NULL,
    is_available BOOLEAN DEFAULT true,
    rating DECIMAL(3,2) DEFAULT 0.0,
    INDEX idx_availability (is_available)
);

-- Create Orders table
CREATE TABLE IF NOT EXISTS Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled') DEFAULT 'pending',
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    payment_method ENUM('cash', 'credit_card', 'debit_card', 'upi', 'wallet') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
    INDEX idx_user (user_id),
    INDEX idx_restaurant_order (restaurant_id),
    INDEX idx_status (status),
    INDEX idx_order_time (order_time)
);

-- Create Order_Items table
CREATE TABLE IF NOT EXISTS Order_Items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    item_price DECIMAL(10,2) NOT NULL,
    special_instructions TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (item_id) REFERENCES Menu_Items(item_id),
    INDEX idx_order (order_id)
);

-- Create Delivery table
CREATE TABLE IF NOT EXISTS Delivery (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    partner_id INT NOT NULL,
    pickup_time DATETIME,
    delivery_time DATETIME,
    delivery_status ENUM('assigned', 'picked_up', 'in_transit', 'delivered', 'cancelled') DEFAULT 'assigned',
    delivery_fee DECIMAL(6,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (partner_id) REFERENCES Delivery_Partners(partner_id),
    INDEX idx_order_delivery (order_id),
    INDEX idx_partner (partner_id),
    INDEX idx_delivery_status (delivery_status)
);

-- Create Reviews table
CREATE TABLE IF NOT EXISTS Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    rating INT N
    OT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
    INDEX idx_user_review (user_id),
    INDEX idx_restaurant_review (restaurant_id)
);

SHOW TABLES;
DESC Users;

INSERT INTO Users (name, email, phone, address, password) VALUES
('John Doe', 'john.doe@example.com', '9876543210', '123 Main St, City', 'password123'),
('Alice Smith', 'alice.smith@example.com', '8765432109', '456 Elm St, Town', 'alicepass'),
('Bob Johnson', 'bob.johnson@example.com', '7654321098', '789 Pine St, Village', 'bobsecure');

INSERT INTO Restaurants (name, address, phone, cuisine_type, rating, opening_hours, closing_hours) VALUES
('Tasty Bites', '101 Food Lane, City', '9988776655', 'Italian', 4.5, '10:00:00', '22:00:00'),
('Spice Garden', '202 Spicy Road, Town', '9876543211', 'Indian', 4.7, '09:00:00', '23:00:00'),
('Sushi Heaven', '303 Ocean Ave, Village', '9765432101', 'Japanese', 4.8, '11:00:00', '21:00:00');

INSERT INTO Menu_Items (restaurant_id, name, description, price, category, is_available, image_url) VALUES
(1, 'Margherita Pizza', 'Classic pizza with fresh tomatoes, mozzarella, and basil', 9.99, 'Pizza', true, 'https://example.com/pizza.jpg'),
(1, 'Pasta Alfredo', 'Creamy Alfredo sauce with fettuccine pasta', 12.99, 'Pasta', true, 'https://example.com/pasta.jpg'),
(2, 'Butter Chicken', 'Rich and creamy butter chicken with naan', 14.99, 'Indian Main Course', true, 'https://example.com/butterchicken.jpg'),
(2, 'Paneer Tikka', 'Grilled paneer cubes marinated in spices', 8.99, 'Appetizer', true, 'https://example.com/paneer.jpg'),
(3, 'Sushi Platter', 'Assorted fresh sushi rolls with soy sauce', 19.99, 'Sushi', true, 'https://example.com/sushi.jpg');

INSERT INTO Delivery_Partners (name, phone, vehicle_type, is_available, rating) VALUES
('Mike Brown', '9998887776', 'Bike', true, 4.6),
('Sarah Lee', '8887776665', 'Scooter', true, 4.8),
('David Kim', '7776665554', 'Car', true, 4.5);

INSERT INTO Orders (user_id, restaurant_id, total_amount, status, payment_status, payment_method) VALUES
(1, 1, 22.98, 'pending', 'pending', 'credit_card'),
(2, 2, 14.99, 'confirmed', 'completed', 'cash'),
(3, 3, 19.99, 'preparing', 'completed', 'upi');

INSERT INTO Order_Items (order_id, item_id, quantity, item_price, special_instructions) VALUES
(1, 1, 1, 9.99, 'Extra cheese'),
(1, 2, 1, 12.99, 'Less salt'),
(2, 3, 1, 14.99, 'Spicy'),
(3, 5, 1, 19.99, 'No wasabi');

INSERT INTO Delivery (order_id, partner_id, pickup_time, delivery_time, delivery_status, delivery_fee) VALUES
(1, 1, NOW(), NULL, 'assigned', 2.50),
(2, 2, NOW(), NOW(), 'delivered', 3.00),
(3, 3, NOW(), NULL, 'in_transit', 2.75);

INSERT INTO Reviews (user_id, restaurant_id, rating, comment) VALUES
(1, 1, 5, 'Amazing food! Highly recommended.'),
(2, 2, 4, 'Great taste, but a bit spicy for me.'),
(3, 3, 5, 'Best sushi in town!');

SELECT * FROM Users;
SELECT * FROM Restaurants;
SELECT * FROM Menu_Items;
SELECT * FROM Orders;
SELECT * FROM Order_Items;
SELECT * FROM Delivery;
SELECT * FROM Reviews;




