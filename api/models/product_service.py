class Product_Service():
    def __init__(self, row):
        self._id = row[0]
        self._name = row[1]
        self._stock  = row[2]
        self._price  = row[3]
        self._description  = row[4]
        self._img = row[5]
        self._type = row[6]
        self._id_user= row[7]

    def to_json(self):
        return {
            "id": self._id,
            "name":self._name,
            "stock": self._stock,
            "price": self._price,
            "description": self._description,
            "img": self._img,
            "type": self._type,
            "id_user": self._id_user,      
        }