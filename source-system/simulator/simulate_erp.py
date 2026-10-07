import os
import random
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

cur = conn.cursor()

action = random.choice(["INSERT", "UPDATE", "CANCEL"])

if action == "INSERT":

    cur.execute("SELECT COALESCE(MAX(order_id), 1000) + 1 FROM orders")
    order_id = cur.fetchone()[0]

    customer_id = random.randint(1, 4)
    quantity = random.randint(10, 250)
    amount = round(quantity * random.uniform(20, 60), 2)

    cur.execute(
        """
        INSERT INTO orders (
            order_id,
            customer_id,
            order_date,
            quantity,
            amount,
            status,
            updated_at
        )
        VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s, 'PENDING', CURRENT_TIMESTAMP)
        """,
        (order_id, customer_id, quantity, amount),
    )

    print(f"INSERT -> order {order_id}")


elif action == "UPDATE":

    cur.execute(
        """
        SELECT order_id
        FROM orders
        WHERE status <> 'CANCELLED'
        ORDER BY RANDOM()
        LIMIT 1
        """
    )

    row = cur.fetchone()

    if row:
        order_id = row[0]
        quantity = random.randint(10, 250)

        cur.execute(
            """
            UPDATE orders
            SET quantity = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE order_id = %s
            """,
            (quantity, order_id),
        )

        print(f"UPDATE -> order {order_id}")


elif action == "CANCEL":

    cur.execute(
        """
        SELECT order_id
        FROM orders
        WHERE status <> 'CANCELLED'
        ORDER BY RANDOM()
        LIMIT 1
        """
    )

    row = cur.fetchone()

    if row:
        order_id = row[0]

        cur.execute(
            """
            UPDATE orders
            SET status = 'CANCELLED',
                updated_at = CURRENT_TIMESTAMP
            WHERE order_id = %s
            """,
            (order_id,),
        )

        print(f"CANCEL -> order {order_id}")


conn.commit()

cur.close()
conn.close()

print(f"Simulation completed at {datetime.now()}")
