class Product_Service():
    def __init__(self, row):
        self._id = row[0]
        self._stock  = row[1]
        self._price  = row[2]
        self._description  = row[3]
        self._img = row[4]
        self._type = row[5]
        self._id_user= row[6]

    def to_json(self):
        return {
            "id": self._id,
            "stock": self._stock,
            "price": self._price,
            "description": self._description,
            "img": self._img,
            "type": self._type,
            "id_user": self._id_user,      
        }