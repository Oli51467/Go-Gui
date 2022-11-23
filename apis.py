import json

import requests

import config


def init_set(data):
    resp = requests.post(url=config.configs['production'].REQUEST_IP + "set", json=data)
    if str(resp).find('502') != -1:
        return False
    return json.loads(resp.text)['code']


def go(data):
    resp = requests.post(url=config.configs['production'].REQUEST_IP + "go", json=data)
    resp_data = json.loads(resp.text)['data']
    print(resp_data)
    return resp_data['pv'][0]
