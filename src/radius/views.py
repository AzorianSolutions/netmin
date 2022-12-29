import json
import pprint
from django.http import HttpRequest, HttpResponse


def action_handler(request: HttpRequest, action: str = None):
    print(f'RADIUS Action: {action}')

    status: int = 200
    data: dict = {
        'config': [],
        'request': [],
        'reply': [],
        'session-state': [],
        'proxy-request': [],
        'proxy-reply': [],
    }

    if action == 'authorize':
        status = 204
        list(data['config']).append(['Auth-Type', 'python3'])

    if action == 'authenticate':
        reply: list = data['reply']
        reply.append(['Framed-IP-Address', '192.168.70.69'])
        reply.append(['Framed-IP-Netmask', '255.255.255.0'])
        # reply.append(['Framed-Route', '10.10.12.0/29'])
        reply.append(['Session-Timeout', '300'])
        reply.append(['Acct-Interim-Interval', '15'])
        reply.append(['Mikrotik-Rate-Limit', '2M/20M'])

    params: dict = {
        'status': status,
    }

    if status is not 204:
        params['content'] = json.dumps(data),
        params['content_type'] = 'application/json'

    return HttpResponse(**params)
