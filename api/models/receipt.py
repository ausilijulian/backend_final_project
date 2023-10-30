class Receipt():
    def __init__(self, row):
        self._id = row[0]
        self._date = row[1]
        self._code = row[2]
        self._id_client= row[3]
        self._id_user= row[4]


    def to_json(self):
        return {
            "id": self._id,
            "date": self._date,
            "code": self._code,
            "id_client": self._id_client,            
            "id_user": self._id_user,      
        }
