import hashlib
import json
import pprint
from django.http import HttpRequest, HttpResponse


def get_payload(request: HttpRequest) -> dict:
    body: dict = json.loads(request.body.decode('UTF-8'))
    payload: dict = {}

    for key, value in body.items():
        payload[key] = {}
        if isinstance(value, list | tuple):
            for item in value:
                payload[key][item[0]] = item[1]

    return payload


def action_handler(request: HttpRequest, action: str = None):
    print(f'RADIUS Action: {action}')
    print('This action is not currently being handled.')
    payload: dict = get_payload(request)
    print(payload)
    return HttpResponse(status=204)


def authenticate(request: HttpRequest):
    from django.db.models import QuerySet
    from accounts.models import AccountEquipment, AccountSubscription

    print(f'RADIUS Action: authenticate')

    key_map: dict = {
        'dhcp': ['Agent-Remote-Id'],
        'ppp-chap': ['User-Name', 'CHAP-Challenge', 'CHAP-Password'],
        'ppp-pap': ['User-Name', 'User-Password'],
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
            user_id: str = str(payload['request']['Agent-Remote-Id']).upper().split('X')[1]
            circuit_id: str = str(payload['request']['Agent-Circuit-Id']).upper().split('X')[1]
            cpe_id: str = str(payload['request']['User-Name']).upper().replace(':', '')

            print(f'Authenticating MAC {cpe_id} via CPE {user_id} and Access Point {circuit_id}')

            registrations: QuerySet = AccountEquipment.objects.filter(mac_address=user_id)
            if registrations.count():
                equipment = registrations[0]

        if auth_type == 'ppp-chap':
            user_id: str = str(payload['request']['User-Name'])
            chap_id: str = str(payload['request']['CHAP-Password'])[2:4]
            chap_password: str = payload['request']['CHAP-Password'][4:]
            chap_challenge: str = str(payload['request']['CHAP-Challenge'])[2:]

            print(f'              User ID: {user_id}')
            print(f'              CHAP ID: {chap_id}')
            print(f'       CHAP Challenge: {chap_challenge}')
            print(f'        CHAP Password: {chap_password}')

            subs: QuerySet = AccountSubscription.objects.filter(username=user_id).order_by('-id')
            if subs.count():
                sub: AccountSubscription = subs[0]
                hasher = hashlib.md5()

                hasher.update(chap_id.encode('ascii'))
                hasher.update(sub.password.encode('ascii'))
                hasher.update(chap_challenge.encode('ascii'))

                print(f'  Test Value (Hashed): {hasher.hexdigest()}')
                print(f'Test Value (Pre-Hash): {chap_id + sub.password + chap_challenge}')

                if chap_password == hasher.hexdigest():
                    subscription = sub
                else:
                    status = 401

        if auth_type == 'ppp-pap':
            user_id: str = str(payload['request']['User-Name'])
            user_password: str = str(payload['request']['User-Password'])
            subs: QuerySet = AccountSubscription.objects.filter(username=user_id, password=user_password) \
                .order_by('-id')
            if subs.count():
                subscription = subs[0]
            else:
                status = 401

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
