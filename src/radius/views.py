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
    from django.db.models import QuerySet
    from accounts.models import AccountEquipment, AccountSubscription

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

    if 'request' not in payload:
        status = 400
    else:
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
        reply: list = response['reply']
        equipment: AccountEquipment | None = None
        subscription: AccountSubscription | None = None
        user_id: str | None = None

        if auth_type == 'dhcp':
            circuit_id: str = str(payload['request']['Agent-Circuit-Id']).upper().split('X')[1]
            remote_id: str = str(payload['request']['Agent-Remote-Id']).upper().split('X')[1]
            cpe_id: str = str(payload['request']['User-Name']).upper().replace(':', '')
            user_id = remote_id

            print(f'Authenticating MAC {cpe_id} via CPE {remote_id} and Access Point {circuit_id}')

            registrations: QuerySet = AccountEquipment.objects.filter(mac_address=remote_id)
            if registrations.count():
                equipment = registrations[0]

        if auth_type == 'ppp':
            username: str = str(payload['request']['User-Name'])
            challenge: str = str(payload['request']['CHAP-Challenge'])
            password: str = str(payload['request']['CHAP-Password'])
            user_id = username

            print(f'Authenticating user {username} via CHAP with challenge {challenge} and password {password}')

            subs: QuerySet = AccountSubscription.objects.filter(username=username)
            if subs.count():
                subscription = subs[0]

        if isinstance(equipment, AccountEquipment):
            subscriptions: QuerySet = AccountSubscription.objects.filter(equipment=equipment).order_by('-id')
            subscription: AccountSubscription | None = None

            if subscriptions.count():
                subscription = subscriptions[0]

        if subscription is None:
            print(f'Could not find subscription for {user_id}')
        else:
            print(f'Found subscription for {user_id} with id {subscription.id}')

            if isinstance(subscription.lease_time, int):
                reply.append(['Session-Timeout', str(subscription.lease_time)])

            if isinstance(subscription.ipv4_address, str):
                reply.append(['Framed-IP-Address', subscription.ipv4_address])
                reply.append(['Framed-IP-Netmask', '255.255.255.0'])

            if isinstance(subscription.ipv4_pool, str):
                reply.append(['Framed-Pool', subscription.ipv4_pool])

            if isinstance(subscription.ipv6_prefix, str):
                reply.append(['Delegated-IPv6-Prefix', subscription.ipv6_prefix])

            if isinstance(subscription.ipv6_pool, str):
                reply.append(['Delegated-IPv6-Prefix-Pool', subscription.ipv6_pool])

            if isinstance(subscription.routes, str):
                reply.append(['Framed-Route', subscription.routes])

            if isinstance(subscription.package.downstream, float) \
                    and isinstance(subscription.package.upstream, float):
                limit: str = f'{int(subscription.package.upstream)}/{int(subscription.package.downstream)}'
                reply.append(['Mikrotik-Rate-Limit', limit])

        reply.append(['Acct-Interim-Interval', '15'])

    params: dict = {
        'status': status,
    }

    if status == 200:
        params['content'] = json.dumps(response),
        params['content_type'] = 'application/json'

    return HttpResponse(**params)
