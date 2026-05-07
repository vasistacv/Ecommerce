-- ═══════════════════════════════════════════════════════════
-- SmartShop E-Commerce — Oracle SQL Schema
-- Compatible with Oracle 19c+ / Oracle XE
-- ═══════════════════════════════════════════════════════════

-- Create tablespace
-- CREATE TABLESPACE ecommerce_ts DATAFILE 'ecommerce_data.dbf' SIZE 500M AUTOEXTEND ON NEXT 100M;

-- Create user
-- CREATE USER ecommerce_user IDENTIFIED BY ecommerce_pass DEFAULT TABLESPACE ecommerce_ts;
-- GRANT CONNECT, RESOURCE, DBA TO ecommerce_user;
-- ALTER USER ecommerce_user QUOTA UNLIMITED ON ecommerce_ts;

-- ═══════════ USER TABLES ═══════════
CREATE TABLE user_profiles (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id NUMBER NOT NULL UNIQUE,
    avatar VARCHAR2(500),
    phone VARCHAR2(20),
    date_of_birth DATE,
    bio VARCHAR2(500),
    loyalty_points NUMBER DEFAULT 0,
    is_premium NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_addresses (
    id RAW(16) DEFAULT SYS_GUID() PRIMARY KEY,
    user_id NUMBER NOT NULL,
    address_type VARCHAR2(10) DEFAULT 'both',
    full_name VARCHAR2(150) NOT NULL,
    street_address VARCHAR2(255) NOT NULL,
    apartment VARCHAR2(100),
    city VARCHAR2(100) NOT NULL,
    state VARCHAR2(100) NOT NULL,
    zip_code VARCHAR2(20) NOT NULL,
    country VARCHAR2(100) DEFAULT 'India',
    phone VARCHAR2(20) NOT NULL,
    is_default NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_activities (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id NUMBER NOT NULL,
    activity_type VARCHAR2(20) NOT NULL,
    product_id RAW(16),
    search_query VARCHAR2(255),
    metadata CLOB CHECK (metadata IS JSON),
    timestamp_col TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════ PRODUCT TABLES ═══════════
CREATE TABLE product_categories (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(200) NOT NULL,
    slug VARCHAR2(200) UNIQUE NOT NULL,
    description CLOB,
    icon VARCHAR2(50),
    image VARCHAR2(500),
    parent_id NUMBER REFERENCES product_categories(id),
    is_active NUMBER(1) DEFAULT 1,
    sort_order NUMBER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id RAW(16) DEFAULT SYS_GUID() PRIMARY KEY,
    name VARCHAR2(300) NOT NULL,
    slug VARCHAR2(300) UNIQUE NOT NULL,
    sku VARCHAR2(50) UNIQUE NOT NULL,
    description CLOB NOT NULL,
    short_description VARCHAR2(500),
    category_id NUMBER NOT NULL REFERENCES product_categories(id),
    brand VARCHAR2(200),
    price NUMBER(12,2) NOT NULL,
    cost_price NUMBER(12,2) DEFAULT 0,
    discount_percent NUMBER(5,2) DEFAULT 0,
    stock NUMBER DEFAULT 0,
    min_stock_alert NUMBER DEFAULT 5,
    weight NUMBER(8,2) DEFAULT 0,
    image VARCHAR2(500),
    is_active NUMBER(1) DEFAULT 1,
    is_featured NUMBER(1) DEFAULT 0,
    tags VARCHAR2(500),
    avg_rating NUMBER(3,2) DEFAULT 0,
    total_reviews NUMBER DEFAULT 0,
    total_sold NUMBER DEFAULT 0,
    views_count NUMBER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_products_category ON products(category_id, is_active);
CREATE INDEX idx_products_created ON products(created_at DESC);

CREATE TABLE product_reviews (
    id RAW(16) DEFAULT SYS_GUID() PRIMARY KEY,
    product_id RAW(16) NOT NULL REFERENCES products(id),
    user_id NUMBER NOT NULL,
    rating NUMBER CHECK (rating BETWEEN 1 AND 5),
    title VARCHAR2(200),
    content CLOB NOT NULL,
    pros CLOB,
    cons CLOB,
    is_verified_purchase NUMBER(1) DEFAULT 0,
    is_approved NUMBER(1) DEFAULT 1,
    helpful_count NUMBER DEFAULT 0,
    sentiment_score NUMBER(4,3),
    sentiment_label VARCHAR2(20),
    is_fake NUMBER(1) DEFAULT 0,
    fake_confidence NUMBER(4,3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_review_user_product UNIQUE (product_id, user_id)
);

CREATE TABLE price_history (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id RAW(16) NOT NULL REFERENCES products(id),
    price NUMBER(12,2) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════ CART TABLES ═══════════
CREATE TABLE shopping_carts (
    id RAW(16) DEFAULT SYS_GUID() PRIMARY KEY,
    user_id NUMBER NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cart_items (
    id RAW(16) DEFAULT SYS_GUID() PRIMARY KEY,
    cart_id RAW(16) NOT NULL REFERENCES shopping_carts(id),
    product_id RAW(16) NOT NULL REFERENCES products(id),
    quantity NUMBER DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_cart_product UNIQUE (cart_id, product_id)
);

-- ═══════════ ORDER TABLES ═══════════
CREATE TABLE orders (
    id RAW(16) DEFAULT SYS_GUID() PRIMARY KEY,
    order_number VARCHAR2(20) UNIQUE NOT NULL,
    user_id NUMBER NOT NULL,
    status VARCHAR2(20) DEFAULT 'pending',
    payment_status VARCHAR2(20) DEFAULT 'pending',
    shipping_name VARCHAR2(150) NOT NULL,
    shipping_address CLOB NOT NULL,
    shipping_city VARCHAR2(100),
    shipping_state VARCHAR2(100),
    shipping_zip VARCHAR2(20),
    shipping_phone VARCHAR2(20),
    subtotal NUMBER(12,2) NOT NULL,
    tax NUMBER(12,2) NOT NULL,
    shipping_cost NUMBER(8,2) DEFAULT 0,
    discount NUMBER(8,2) DEFAULT 0,
    total NUMBER(12,2) NOT NULL,
    fraud_score NUMBER(4,3),
    fraud_flagged NUMBER(1) DEFAULT 0,
    fraud_reason CLOB,
    notes CLOB,
    tracking_number VARCHAR2(100),
    estimated_delivery DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id RAW(16) DEFAULT SYS_GUID() PRIMARY KEY,
    order_id RAW(16) NOT NULL REFERENCES orders(id),
    product_id RAW(16) REFERENCES products(id),
    product_name VARCHAR2(300) NOT NULL,
    product_sku VARCHAR2(50),
    quantity NUMBER NOT NULL,
    unit_price NUMBER(12,2) NOT NULL,
    total_price NUMBER(12,2) NOT NULL
);

CREATE TABLE order_tracking (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id RAW(16) NOT NULL REFERENCES orders(id),
    status VARCHAR2(50) NOT NULL,
    description CLOB NOT NULL,
    location VARCHAR2(200),
    timestamp_col TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════ PAYMENT TABLE ═══════════
CREATE TABLE payments (
    id RAW(16) DEFAULT SYS_GUID() PRIMARY KEY,
    order_id RAW(16) NOT NULL UNIQUE REFERENCES orders(id),
    user_id NUMBER NOT NULL,
    transaction_id VARCHAR2(100) UNIQUE NOT NULL,
    payment_method VARCHAR2(20) NOT NULL,
    amount NUMBER(12,2) NOT NULL,
    currency VARCHAR2(3) DEFAULT 'INR',
    status VARCHAR2(20) DEFAULT 'initiated',
    card_last_four VARCHAR2(4),
    card_brand VARCHAR2(20),
    metadata CLOB CHECK (metadata IS JSON),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════ WAREHOUSE TABLES ═══════════
CREATE TABLE warehouses (
    id RAW(16) DEFAULT SYS_GUID() PRIMARY KEY,
    name VARCHAR2(200) NOT NULL,
    code VARCHAR2(20) UNIQUE NOT NULL,
    address CLOB,
    city VARCHAR2(100),
    state VARCHAR2(100),
    capacity NUMBER NOT NULL,
    current_occupancy NUMBER DEFAULT 0,
    manager_name VARCHAR2(150),
    manager_phone VARCHAR2(20),
    is_active NUMBER(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE warehouse_inventory (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    warehouse_id RAW(16) NOT NULL REFERENCES warehouses(id),
    product_id RAW(16) NOT NULL REFERENCES products(id),
    quantity NUMBER DEFAULT 0,
    reserved NUMBER DEFAULT 0,
    reorder_level NUMBER DEFAULT 10,
    last_restocked TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_wh_product UNIQUE (warehouse_id, product_id)
);

CREATE TABLE shipments (
    id RAW(16) DEFAULT SYS_GUID() PRIMARY KEY,
    order_id RAW(16) NOT NULL REFERENCES orders(id),
    warehouse_id RAW(16) NOT NULL REFERENCES warehouses(id),
    tracking_number VARCHAR2(100),
    carrier VARCHAR2(100),
    status VARCHAR2(20) DEFAULT 'preparing',
    weight NUMBER(8,2) DEFAULT 0,
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════ VIEWS ═══════════
CREATE OR REPLACE VIEW v_product_analytics AS
SELECT p.id, p.name, p.sku, c.name AS category, p.brand,
       p.price, p.stock, p.avg_rating, p.total_sold, p.views_count,
       p.total_reviews, p.discount_percent,
       CASE WHEN p.stock <= p.min_stock_alert THEN 'LOW' ELSE 'OK' END AS stock_status
FROM products p JOIN product_categories c ON p.category_id = c.id
WHERE p.is_active = 1;

CREATE OR REPLACE VIEW v_order_summary AS
SELECT o.id, o.order_number, o.status, o.payment_status,
       o.total, o.fraud_score, o.fraud_flagged,
       o.created_at, COUNT(oi.id) AS item_count
FROM orders o LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, o.order_number, o.status, o.payment_status, o.total, o.fraud_score, o.fraud_flagged, o.created_at;

COMMIT;
