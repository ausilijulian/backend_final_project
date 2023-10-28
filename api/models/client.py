class Client():
    def __init__(self, row):
        self._id = row[0]
        self._name  = row[1]
        self._surname  = row[2]
        self._email  = row[3]
        self._dni= row[4]
        self._id_user= row[5]

    def to_json(self):
        return {
            "id": self._id,
            "name": self._name,
            "surname": self._surname,
            "email": self._email,
            "dni": self._dni,
            "id_user": self._id_user,      
        }