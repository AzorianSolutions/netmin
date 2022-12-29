import json
import pprint
from django.http import HttpRequest, HttpResponse


def get_payload(request: HttpRequest) -> dict:
    body: dict = json.loads(request.body.decode('UTF-8'))
    payload: dict = {}

    for key, value in body.items():
        payload[key] = {}
        if isinstance(value, list|tuple):
            for item in value:
                payload[key][item[0]] = item[1]

    return payload


def action_handler(request: HttpRequest, action: str = None):
    print(f'RADIUS Action: {action}')
    print('This action is not currently being handled.')
    return HttpResponse(status=204)


def authenticate(request: HttpRequest):
    print(f'RADIUS Action: authenticate')

    key_map: dict = {
        'dhcp': ['Agent-Remote-Id'],
        'ppp': ['User-Name', 'CHAP-Challenge', 'CHAP-Password'],
    }
    payload: dict = get_payload(request)
    auth_type: str | None = None
    status: int = 200
    response: dict = {
        'config': [],
        'request': [],
        'reply': [],
        'session-state': [],
        'proxy-request': [],
        'proxy-reply': [],
    }

    for key, value in key_map.items():
        valid: bool = True
        for item in value:
            if item not in payload['request']:
                valid = False
                break

        if valid:
            auth_type = key
            break

    if auth_type is None:
        status = 400

    if status == 200:

        if auth_type == 'dhcp':
            pass

        if auth_type == 'ppp':
            pass

        reply: list = response['reply']
        reply.append(['Framed-IP-Address', '192.168.70.69'])
        reply.append(['Framed-IP-Netmask', '255.255.255.0'])
        # reply.append(['Framed-Route', '10.10.12.0/29'])
        reply.append(['Session-Timeout', '300'])
        reply.append(['Acct-Interim-Interval', '15'])
        reply.append(['Mikrotik-Rate-Limit', '2M/20M'])

    params: dict = {
        'status': status,
    }

    if status == 200:
        params['content'] = json.dumps(response),
        params['content_type'] = 'application/json'

    return HttpResponse(**params)
