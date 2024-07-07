CREATE SCHEMA pre_prd;

CREATE SCHEMA prd;

CREATE TABLE pre_prd.product_catalog (
    product_id VARCHAR(10) NOT NULL,
    product_name VARCHAR(255) NOT NULL,	
    category VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    created_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
    created_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
    updated_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
    updated_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
    CONSTRAINT product_product_id_pkey PRIMARY KEY(product_id)
);

CREATE TABLE pre_prd.customer_transactions (
    transaction_id VARCHAR(255) NOT NULL,
    customer_id VARCHAR(10) NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    "timestamp" TIMESTAMP,
    created_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
    created_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
    updated_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
    updated_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
    CONSTRAINT customer_transactions_transaction_id_pkey PRIMARY KEY(transaction_id),
    CONSTRAINT customer_transaction_product_id_fkey FOREIGN KEY (product_id) REFERENCES pre_prd.product_catalog(product_id)
);

CREATE TABLE prd.product_sales_detail (
    transaction_id VARCHAR(255) NOT NULL,
    customer_id VARCHAR(10) NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    total_price FLOAT NOT NULL,
    transaction_date DATE NOT NULL,
    created_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
    created_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
    updated_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
    updated_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
    CONSTRAINT product_sales_detail_transaction_id_pkey PRIMARY KEY(transaction_id),
    CONSTRAINT product_sales_detail_product_id_fkey FOREIGN KEY (product_id) REFERENCES pre_prd.product_catalog(product_id)
);
