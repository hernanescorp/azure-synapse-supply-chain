INSERT INTO customers
    (customer_id, customer_name, country)
VALUES
    (1, 'Toyota', 'Japan'),
    (2, 'BMW', 'Germany'),
    (3, 'Stellantis', 'Netherlands'),
    (4, 'Mercedes-Benz', 'Germany');


INSERT INTO orders
    (order_id, customer_id, order_date, quantity, amount, status)
VALUES
    (1001, 1, CURRENT_TIMESTAMP - INTERVAL '3 days', 120, 5400.00, 'CONFIRMED'),
    (1002, 2, CURRENT_TIMESTAMP - INTERVAL '2 days', 80, 4200.00, 'CONFIRMED'),
    (1003, 3, CURRENT_TIMESTAMP - INTERVAL '1 day', 200, 7600.00, 'PENDING'),
    (1004, 4, CURRENT_TIMESTAMP, 50, 3100.00, 'PENDING');
