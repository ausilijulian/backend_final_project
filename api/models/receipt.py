
from api.db.db import mysql

class Receipt:
    def __init__(self, receipt_row, detail_rows):
        self._id = receipt_row[0]
        self._date = receipt_row[1]
        self._code = receipt_row[2]
        self._id_client = receipt_row[3]
        self._id_user = receipt_row[4]

        self._details = []  # Inicialmente, no hay detalles

        if detail_rows:
            for row in detail_rows:
                cur = mysql.connection.cursor()
                cur.execute('SELECT name FROM product_service WHERE id = %s', (row[2],))
                name_product = cur.fetchone()
                cur.execute('SELECT type FROM product_service WHERE id = %s', (row[2],))
                type_product = cur.fetchone()
                detail = {
                    "id_product_service": row[2],
                    "name": name_product[0],
                    "type": type_product[0],
                    "quantity": row[3],
                    "unit_price": row[4]
                }
                self._details.append(detail)

    def to_json(self):
        receipt_data = {
            "id": self._id,
            "date": self._date,
            "code": self._code,
            "id_client": self._id_client,
            "id_user": self._id_user,
            "details": self._details
        }

        return receipt_data