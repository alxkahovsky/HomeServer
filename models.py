from db_manager import BaseModel


class Room(BaseModel):
    fields = ['room', 'devices']
    collection = 'ROOM'
    unique_fields = ['room']
