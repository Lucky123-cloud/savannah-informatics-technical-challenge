from fastapi import HTTPException
from datetime import datetime
import psycopg2
from psycopg2.extras import DictCursor
from typing import Optional

from configs.database import InitDB

class OrderRepository(InitDB):
    """This class handles data manipulation in the orders table"""

    def __init__(self):
        # Call the connect method of the base class
        # to create a database connection
        self.conn = self.connect()

    def create_order(
            self,
            customer_id: int,
            order_price: float,
            item_id: int
        ):
        """Creates a new order in the database"""

        sql_context = """
        INSERT INTO
            orders (customer_id, total_amount, product_id)
        VALUES
            (%s, %s, %s);
        """
        data = (customer_id, order_price, item_id)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql_context, data)

            self.conn.commit()
        except psycopg2.DataError:
            raise HTTPException(
                    status_code=400,
                    detail="A data error occured, possibly due to invalid valus"
                )
        except psycopg2.Error as e:
            print(e)
            raise HTTPException(
                    status_code=500,
                    detail="An error occured while creating your order"
                )

    def get_order_by_id(self, order_id: str):
        """Gets a specific order by its id"""

        sql_context = """
        SELECT
            order_date, product_id, total_amount
        FROM
            orders
        WHERE
            id = %s;
        """
        data = (order_id,)

        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(sql_context, data)
                order = cursor.fetchone()

            self.conn.commit()
            return order
        except psycopg2.Error:
            raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occured while retrieving the order"
                )

    def delete_order_by_id(self, order_id: str):
        """Deletes an order record from the database"""

        sql_context = """
        DELETE FROM
            orders
        WHERE
            id = %s;
        """
        data = (order_id,)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql_context, data)

            self.conn.commit()
            return
        except psycopg2.Error:
            pass
