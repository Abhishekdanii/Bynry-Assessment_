-- Bynry Backend Assessment
-- Inventory Management Database

CREATE DATABASE IF NOT EXISTS bynry;
USE bynry;

-- =========================
-- TABLES
-- =========================

CREATE TABLE IF NOT EXISTS companies (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS warehouses (
    id CHAR(36) PRIMARY KEY,
    company_id CHAR(36),
    name VARCHAR(255) NOT NULL,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
        ON DELETE CASCADE
);

-- PRODUCTS
-- =========================
CREATE TABLE IF NOT EXISTS products (
    id CHAR(36) PRIMARY KEY,
    company_id CHAR(36),
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL,
    low_stock_threshold INT DEFAULT 10,
    is_bundle BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
        ON DELETE CASCADE
);

-- INVENTORY (CORE TABLE)
-- =========================
CREATE TABLE IF NOT EXISTS inventory (
    id CHAR(36) PRIMARY KEY,
    product_id CHAR(36),
    warehouse_id CHAR(36),
    quantity INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE(product_id, warehouse_id),

    FOREIGN KEY (product_id) REFERENCES products(id)
        ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
        ON DELETE CASCADE
);

-- INVENTORY LOGS (AUDIT TRAIL)
-- =========================
CREATE TABLE IF NOT EXISTS inventory_logs (
    id CHAR(36) PRIMARY KEY,
    product_id CHAR(36),
    warehouse_id CHAR(36),
    change_quantity INT,
    reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

-- SUPPLIERS
-- =========================
CREATE TABLE IF NOT EXISTS suppliers (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PRODUCT-SUPPLIER (MANY-TO-MANY)
-- =========================
CREATE TABLE IF NOT EXISTS product_suppliers (
    product_id CHAR(36),
    supplier_id CHAR(36),

    PRIMARY KEY (product_id, supplier_id),

    FOREIGN KEY (product_id) REFERENCES products(id)
        ON DELETE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        ON DELETE CASCADE
);

-- PRODUCT BUNDLES
-- =========================
CREATE TABLE IF NOT EXISTS product_bundles (
    parent_product_id CHAR(36),
    child_product_id CHAR(36),
    quantity INT DEFAULT 1,

    PRIMARY KEY (parent_product_id, child_product_id),

    FOREIGN KEY (parent_product_id) REFERENCES products(id),
    FOREIGN KEY (child_product_id) REFERENCES products(id)
);

-- SALES
-- =========================
CREATE TABLE IF NOT EXISTS sales (
    id CHAR(36) PRIMARY KEY,
    product_id CHAR(36),
    quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- =========================
-- DEBUG / STRUCTURE CHECK
-- =========================
SHOW TABLES;
DESCRIBE products;
SHOW CREATE TABLE inventory;

-- =========================
-- SAMPLE DATA (SAFE INSERT)
-- =========================

INSERT IGNORE INTO companies (id, name)
VALUES ('c1', 'Demo Company');

INSERT IGNORE INTO warehouses (id, company_id, name)
VALUES ('w1', 'c1', 'Main Warehouse');

INSERT IGNORE INTO products (id, company_id, name, sku, price, low_stock_threshold)
VALUES ('p1', 'c1', 'Widget A', 'WID-001', 100.00, 20);

INSERT IGNORE INTO inventory (id, product_id, warehouse_id, quantity)
VALUES ('i1', 'p1', 'w1', 5);

INSERT IGNORE INTO suppliers (id, name, contact_email)
VALUES ('s1', 'Supplier Corp', 'orders@supplier.com');

INSERT IGNORE INTO product_suppliers (product_id, supplier_id)
VALUES ('p1', 's1');

INSERT IGNORE INTO sales (id, product_id, quantity, created_at)
VALUES ('sale1', 'p1', 10, NOW());

-- =========================
-- LOW STOCK QUERY (OUTPUT)
-- =========================
SELECT 
    p.name,
    i.quantity,
    p.low_stock_threshold
FROM products p
JOIN inventory i ON p.id = i.product_id
WHERE i.quantity < p.low_stock_threshold;