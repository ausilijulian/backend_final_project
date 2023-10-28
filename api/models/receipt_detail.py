class Receipt_Detail():
    def __init__(self, row):
        self._id = row[0]
        self._id_receipt = row[1]
        self._id_product_service = row[2]
        self._quantity = row[3]
        self._unit_price = row[4]

    def to_json(self):
        return {
            "id": self._id,
            "id_receipt": self._id_receipt,
            "id_product_service": self._id_product_service,            
            "quantity": self._quantity,     
            "unit_price": self._unit_price,     
        }