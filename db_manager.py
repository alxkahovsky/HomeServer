from pymongo import MongoClient


def get_database():
    # Укажите URL-адрес mongodb atlas для подключения python к mongodb с помощью pymongo
    # Или оставьте пустым для использования локальной БД
    CONNECTION_URL = ''
    # Укажите IP-адрес и порт. Указынны значения по умолчанию, см. файл конфигурации ur-mongodb/bin/mongod.cfg
    IP, PORT = "localhost", 27017
    # Укажите название базы данных
    DB_NAME = 'HSS'
    if CONNECTION_URL == '':
        CONNECTION_URL = f'{IP}:{PORT}'
    client = MongoClient(CONNECTION_URL)
    return client[DB_NAME]


if __name__ == "__main__":
    dbname = get_database()
