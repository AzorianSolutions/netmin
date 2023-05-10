import json
import radiusd
import requests
from requests import Response


def convert_payload(source: dict) -> dict:
    payload: dict = {}
    if not isinstance(source, dict):
        return payload

    for key, value in source.items():
        if isinstance(value, list):
            payload[key] = tuple(tuple(sub) for sub in value)

    return payload


def call_api(action: str, payload: dict) -> tuple:
    res: Response = requests.get(radiusd.config['api']['base_uri'] + f'/{action}', json=payload)
    res_data: dict = json.loads(res.content) if len(res.content) else {'status': 7, 'payload': {}}
    return int(res_data['status']), convert_payload(res_data)


def instantiate(p: dict):
    return 0


def authorize(p: dict):
    radiusd.radlog(radiusd.L_INFO, f'netmin: authorize')
    response: tuple = call_api('authorize', p)
    return response[0], response[1]


def authenticate(p: dict):
    radiusd.radlog(radiusd.L_INFO, 'netmin: authenticate')
    response: tuple = call_api('authenticate', p)
    return response[0], response[1]


def preacct(p: dict):
    radiusd.radlog(radiusd.L_INFO, 'netmin: preacct')
    response: tuple = call_api('preacct', p)
    return response[0], response[1]


def checksimul(p: dict):
    radiusd.radlog(radiusd.L_INFO, 'netmin: checksimul')
    response: tuple = call_api('checksimul', p)
    return response[0], response[1]


def accounting(p: dict):
    radiusd.radlog(radiusd.L_INFO, f'netmin: accounting')
    response: tuple = call_api('accounting', p)
    return response[0], response[1]


def pre_proxy(p: dict):
    radiusd.radlog(radiusd.L_INFO, f'netmin: pre_proxy')
    response: tuple = call_api('pre_proxy', p)
    return response[0], response[1]


def post_proxy(p: dict):
    radiusd.radlog(radiusd.L_INFO, f'netmin: post_proxy')
    response: tuple = call_api('post_proxy', p)
    return response[0], response[1]


def post_auth(p: dict):
    radiusd.radlog(radiusd.L_INFO, f'netmin: post_auth')
    response: tuple = call_api('post_auth', p)
    return response[0], response[1]


def recv_coa(p: dict):
    radiusd.radlog(radiusd.L_INFO, f'netmin: recv_coa')
    response: tuple = call_api('recv_coa', p)
    return response[0], response[1]


def send_coa(p: dict):
    radiusd.radlog(radiusd.L_INFO, f'netmin: send_coa')
    response: tuple = call_api('send_coa', p)
    return response[0], response[1]


def detach(p: dict):
    radiusd.radlog(radiusd.L_INFO, f'netmin: detach')
    response: tuple = call_api('detach', p)
    return response[0], response[1]
