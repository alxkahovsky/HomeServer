import json

from fastapi import Body
from db_manager import get_database


class Room(object):
    __db = get_database()['ROOM']

    def __init__(self, data):
        self._id = data['id']
        self.devices = data.get('devices')

    def create(self):
        document = {'_id': self._id, 'devices': self.devices}
        self.__db.insert_one(document)
        return document

    def read(self):
        return self.__db.find_one({'_id': self._id})

    def update(self):
        self.__db.update_one({'_id': self._id}, {'$set': {'devices': self.devices}})
        return self.read()
