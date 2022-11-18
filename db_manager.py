from pymongo import MongoClient
import settings


class BaseModel():
    __connection = settings.db_config['connection']
    __ip, __port = settings.db_config['ip, port']
    __db_name = settings.db_config['db_name']
    collection: str = None
    fields: list = None
    unique_fields: list = None

    def get_database(self):
        if self.__connection == '':
            self.__connection = f'{self.__ip}:{self.__port}'
        client = MongoClient(self.__connection)
        return client[self.__db_name][self.collection]

    def __init__(self, data):
        if isinstance(data, dict):
            for key in data.keys():
                if key not in self.fields:
                    raise Exception("ValidationError: поля не совпадают")
        else:
            raise Exception("TypeError: Неверный тип данных")
        self.__db = self.get_database()
        if self.unique_fields:
            for unique in self.unique_fields:
                self.__db.create_index(unique, unique=True)
        self.data = data

    def read(self):
        result = self.__db.find_one(self.data)
        result["_id"] = str(result["_id"])
        return result

    def create(self):
        self.__db.insert_one(self.data)
        return self.read()

    def update(self):
        data_tuple = tuple(self.data.items())[0]
        for k,v in self.data.items():
            if isinstance(v, dict):
                self.__db.update_one({data_tuple[0]: self.data[data_tuple[0]]}, {'$set': {k: v}})
        return self.read()

    def db_info(self):
        print(f'MongoDB, base name: {self.__db_name}, connection: {self.__connection}')


if __name__ == "__main__":
    db = BaseModel({})
