import json
import pprint
from django.http import HttpRequest, HttpResponse


def action_handler(request: HttpRequest, action: str = None):
    print(f'RADIUS: {action}')

    status: int = 200
    data: dict = {
        'reply': [],
    }

    if action == 'authorize':
        status = 204

    if action == 'authenticate':
        reply: list = data['reply']
        reply.append(['Framed-IP-Address', '192.168.70.69'])
        reply.append(['Framed-IP-Netmask', '255.255.255.0'])
        # reply.append(['Framed-Route', '10.10.11.1/32'])
        reply.append(['Session-Timeout', '60'])
        reply.append(['Acct-Interim-Interval', '15'])
        reply.append(['Mikrotik-Rate-Limit', '2M/20M'])

    pprint.pp(dict(request.GET.items()))

    return HttpResponse(json.dumps(data), status=status, content_type='application/json')
