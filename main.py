from copy import copy
import requests
from e3372h import Client
from fastapi import BackgroundTasks, FastAPI, Body
from fastapi_utils.tasks import repeat_every
import random
import asyncio
from pywizlight import wizlight, PilotBuilder, discovery
import itertools
from db_manager import get_database
import json
from models import Room


application = FastAPI()


@application.get('/modem_status')
def get_modem_status():
    modem = Client()
    if modem.is_hilink():
        raw_signal_data = modem.device_signal()
        signal_data = {'STATUS': 'Ok',
                       'RSSI': raw_signal_data.rssi,
                       'SINR': raw_signal_data.sinr,
                       'RSRP': raw_signal_data.rsrp,
                       'RSRQ': raw_signal_data.rsrq
                       }
    else:
        # signal_data = {'STATUS': 'Failed',
        #                'RSSI': None,
        #                'SINR': None,
        #                'RSRP': None,
        #                'RSRQ': None
        #                }
        # dev_mode working without house LAN
        signal_data = {'STATUS': 'Ok',
                       'RSSI': random.randint(1,100),
                       'SINR': random.randint(1,100),
                       'RSRP': random.randint(1,100),
                       'RSRQ': random.randint(1,100)
                       }
    print(signal_data)
    return signal_data

# testin cycle tasks, async tasks
# @application.on_event("startup")
# @repeat_every(seconds=5.0)
# def cycle_task() -> None:
#     print('хобана цикличная задача')
#
#
# @application.get('/')
# def hello_world():
#     return 'Hello World!'


# @application.get('/test')
# async def test_bgtask(background_tasks: BackgroundTasks):
#     background_tasks.add_task(background_task)
#     return {"message": "Email Log Entry Created by Background Task"}

@application.get('/bulbs')
async def get_bulbs() -> dict:
    """ возвращает сериализированные данные по лампам в сети"""
    bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
    result = {i+1: dict(itertools.islice(bulbs[i].__dict__.items(), 4)) for i in range(0, len(bulbs))}
    return result


@application.post('/create_room')
def create_room(data: dict = Body()):
    """
    Создание объекта комнаты.
    Пример данных ввода: {"id":"Название", "devices":dict}, параметр "devices" - необязательный.
    Для создания пустой комнаты не указывайте его.
    Пример данных вывода: {"id":"Название", "devices":dict}.
    """
    room = Room(data)
    return room.create()


@application.get('/room/{room_id}')
def get_room(room_id: str):
    room = Room({'id': room_id})
    return room.read()


@application.patch('/add_room_device')
def bind_device(data: dict = Body()):
    room = Room(data)
    return room.update()
