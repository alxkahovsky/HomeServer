from e3372h import Client
from fastapi import FastAPI


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
        signal_data = {'STATUS': 'Failed',
                       'RSSI': None,
                       'SINR': None,
                       'RSRP': None,
                       'RSRQ': None
                       }
    return signal_data


