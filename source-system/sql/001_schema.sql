CREATE TABLE customers (
    customer_id     INTEGER PRIMARY KEY,
    customer_name   VARCHAR(100) NOT NULL,
    country         VARCHAR(50) NOT NULL
);

CREATE TABLE orders (
    order_id        BIGINT PRIMARY KEY,
    customer_id     INTEGER NOT NULL,
    order_date      TIMESTAMP NOT NULL,
    quantity        INTEGER NOT NULL,
    amount          NUMERIC(12,2) NOT NULL,
    status          VARCHAR(20) NOT NULL,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE INDEX idx_orders_updated_at
    ON orders(updated_at);
