import json
import radiusd
import requests
from requests import Response


def execute_request(action: str, payload: str) -> Response:
    return requests.get(radiusd.config['api']['base_uri'] + f'/{action}', params=payload)


def extract_response(response: Response) -> dict:
    result: dict | None = None

    if len(response.content):
        result = json.loads(response.content)

    return result


def convert_response(response: dict) -> dict:
    if not isinstance(response, dict):
        return response

    for key, value in response.items():
        if isinstance(value, list):
            response[key] = tuple(tuple(sub) for sub in value)

    return response


def instantiate(p):
    return 0


def authorize(p):
    radiusd.radlog(radiusd.L_INFO, f'netmin: authorize')
    response: dict = convert_response(extract_response(execute_request('authorize', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response


def authenticate(p):
    radiusd.radlog(radiusd.L_INFO, 'netmin: authenticate')
    response: dict = convert_response(extract_response(execute_request('authenticate', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response


def preacct(p):
    radiusd.radlog(radiusd.L_INFO, 'netmin: preacct')
    response: dict = convert_response(extract_response(execute_request('preacct', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response


def checksimul(p):
    radiusd.radlog(radiusd.L_INFO, 'netmin: checksimul')
    response: dict = convert_response(extract_response(execute_request('checksimul', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response


def accounting(p):
    radiusd.radlog(radiusd.L_INFO, f'netmin: accounting')
    response: dict = convert_response(extract_response(execute_request('accounting', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response


def pre_proxy(p):
    radiusd.radlog(radiusd.L_INFO, f'netmin: pre_proxy')
    response: dict = convert_response(extract_response(execute_request('pre_proxy', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response


def post_proxy(p):
    radiusd.radlog(radiusd.L_INFO, f'netmin: post_proxy')
    response: dict = convert_response(extract_response(execute_request('post_proxy', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response


def post_auth(p):
    radiusd.radlog(radiusd.L_INFO, f'netmin: post_auth')
    response: dict = convert_response(extract_response(execute_request('post_auth', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response


def recv_coa(p):
    radiusd.radlog(radiusd.L_INFO, f'netmin: recv_coa')
    response: dict = convert_response(extract_response(execute_request('recv_coa', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response


def send_coa(p):
    radiusd.radlog(radiusd.L_INFO, f'netmin: send_coa')
    response: dict = convert_response(extract_response(execute_request('send_coa', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response


def detach(p):
    radiusd.radlog(radiusd.L_INFO, f'netmin: detach')
    response: dict = convert_response(extract_response(execute_request('detach', json.dumps(p))))
    return radiusd.RLM_MODULE_OK, response
