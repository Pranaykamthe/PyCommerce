"""
Creates all database tables required by PyCommerce.

Tables:
1. users
2. categories
3. products
4. cart
5. orders
6. order_items
7. payments
8. reviews
9. wishlist
"""

from mysql.connector import Error

from config.database import (
    create_database,
    get_connection,
    close_connection
)


# ============================================================
# TABLE CREATION QUERIES
# ============================================================

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    role ENUM('customer', 'admin') NOT NULL DEFAULT 'customer',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
"""


CREATE_CATEGORIES_TABLE = """
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
"""


CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    image_path VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_product_price
        CHECK (price >= 0),

    CONSTRAINT chk_product_stock
        CHECK (stock_quantity >= 0),

    INDEX idx_products_category (category_id),
    INDEX idx_products_name (product_name)
);
"""


CREATE_CART_TABLE = """
CREATE TABLE IF NOT EXISTS cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_cart_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_cart_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT uq_cart_user_product
        UNIQUE (user_id, product_id),

    CONSTRAINT chk_cart_quantity
        CHECK (quantity > 0),

    INDEX idx_cart_user (user_id),
    INDEX idx_cart_product (product_id)
);
"""


CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    order_status ENUM(
        'pending',
        'confirmed',
        'shipped',
        'delivered',
        'cancelled'
    ) NOT NULL DEFAULT 'pending',
    shipping_address TEXT NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_order_total
        CHECK (total_amount >= 0),

    INDEX idx_orders_user (user_id),
    INDEX idx_orders_status (order_status),
    INDEX idx_orders_date (order_date)
);
"""


CREATE_ORDER_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_order_item_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_order_item_unit_price
        CHECK (unit_price >= 0),

    CONSTRAINT chk_order_item_subtotal
        CHECK (subtotal >= 0),

    INDEX idx_order_items_order (order_id),
    INDEX idx_order_items_product (product_id)
);
"""


CREATE_PAYMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_method ENUM(
        'cash',
        'card',
        'upi',
        'net_banking'
    ) NOT NULL,
    payment_status ENUM(
        'pending',
        'successful',
        'failed',
        'refunded'
    ) NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR(100) UNIQUE,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_payment_amount
        CHECK (amount >= 0),

    INDEX idx_payments_order (order_id),
    INDEX idx_payments_status (payment_status)
);
"""


CREATE_REVIEWS_TABLE = """
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL,
    review_text TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_reviews_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_reviews_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT uq_review_user_product
        UNIQUE (user_id, product_id),

    CONSTRAINT chk_review_rating
        CHECK (rating BETWEEN 1 AND 5),

    INDEX idx_reviews_product (product_id),
    INDEX idx_reviews_user (user_id)
);
"""


# ============================================================
# WISHLIST TABLE
# ============================================================

CREATE_WISHLIST_TABLE = """
CREATE TABLE IF NOT EXISTS wishlist (
    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_wishlist_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_wishlist_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT uq_wishlist_user_product
        UNIQUE (user_id, product_id),

    INDEX idx_wishlist_user (user_id),
    INDEX idx_wishlist_product (product_id)
);
"""


# ============================================================
# TABLE CREATION ORDER
# ============================================================

TABLES = [
    ("users", CREATE_USERS_TABLE),
    ("categories", CREATE_CATEGORIES_TABLE),
    ("products", CREATE_PRODUCTS_TABLE),
    ("cart", CREATE_CART_TABLE),
    ("orders", CREATE_ORDERS_TABLE),
    ("order_items", CREATE_ORDER_ITEMS_TABLE),
    ("payments", CREATE_PAYMENTS_TABLE),
    ("reviews", CREATE_REVIEWS_TABLE),
    ("wishlist", CREATE_WISHLIST_TABLE),
]


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables() -> bool:
    """
    Create all PyCommerce tables.

    Returns:
        bool: True if all tables are created successfully,
              otherwise False.
    """

    connection = get_connection()

    if connection is None:
        print("[ERROR] Cannot create tables without database connection.")
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        for table_name, query in TABLES:
            cursor.execute(query)
            print(f"[SUCCESS] Table '{table_name}' is ready.")

        connection.commit()

        print("[SUCCESS] All PyCommerce tables are ready.")

        return True

    except Error as e:
        connection.rollback()

        print("[ERROR] Failed to create database tables.")
        print(e)

        return False

    finally:
        if cursor is not None:
            cursor.close()

        close_connection(connection)


# ============================================================
# MAIN
# ============================================================

def initialize_database() -> bool:
    """
    Create the database and all required tables.

    Returns:
        bool: True if initialization succeeds.
    """

    create_database()

    return create_tables()


if __name__ == "__main__":
    initialize_database()