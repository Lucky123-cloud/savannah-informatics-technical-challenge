-- This script creates sql tables in the database


-- Create a customers table if it does not exist in the db
CREATE TABLE IF NOT EXISTS customers (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	password VARCHAR(200),
	phone VARCHAR(15) NOT NULL,
	created_at DATE DEFAULT NOW()
);

-- Create a products table if it does not exist in the db
CREATE TABLE IF NOT EXISTS products (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	description VARCHAR(200) NOT NULL,
	price DECIMAL(10, 2) NOT NULL,
	stock_quantity INTEGER DEFAULT 0
);

-- Create an orders table if it does not exist in the db
CREATE TABLE IF NOT EXISTS orders (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	total_amount DECIMAL(10, 2) NOT NULL,
	customer_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	FOREIGN KEY (product_id) REFERENCES products (id),
	FOREIGN KEY (customer_id) REFERENCES customers (id)
);
