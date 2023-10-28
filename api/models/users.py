class Users():
    def __init__(self, row):
        self._id = row[0]
        self._username = row[1]
        self._email= row[2]
        self._password= row[3]

    def to_json(self):
        return {
            "id": self._id,
            "date": self._username,
            "id_client": self._email,            
            "id_user": self._password,      
        }