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


def authenticate(req: HttpRequest):
    from django.db.models import QuerySet
    from accounts.models import AccountEquipment, AccountSubscription
    from radius.clients.freeradius.mutables import NetminRequest, NetminResponse

    print(f'RADIUS Action: authenticate')

    auth_type: str | None = None
    key_map: dict = {
        'dhcp': ['Agent-Remote-Id'],
        'ppp-chap': ['User-Name', 'CHAP-Challenge', 'CHAP-Password'],
        'ppp-pap': ['User-Name', 'User-Password'],
    }
    payload: dict = get_payload(req)
    request: NetminRequest = NetminRequest.loads(req.body.decode('UTF-8'))
    response: NetminResponse = NetminResponse()

    if 'request' not in payload:
        response.status = 4
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
        response.status = 4

    if response.status in [2, 3, 7, 8]:
        user_id: str | None = None
        equipment: AccountEquipment | None = None
        subscription: AccountSubscription | None = None

        if auth_type == 'dhcp':
            user_id: str = str(payload['request']['Agent-Remote-Id']).upper().split('X')[1]
            circuit_id: str = str(payload['request']['Agent-Circuit-Id']).upper().split('X')[1]
            cpe_id: str = str(payload['request']['User-Name']).upper().replace(':', '')

            print(f'   User ID: {user_id}')
            print(f'Circuit ID: {circuit_id}')
            print(f'    CPE ID: {cpe_id}')

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
                    response.status = 0

        if auth_type == 'ppp-pap':
            user_id: str = str(payload['request']['User-Name'])
            user_password: str = str(payload['request']['User-Password'])
            subs: QuerySet = AccountSubscription.objects.filter(username=user_id, password=user_password) \
                .order_by('-id')
            if subs.count():
                subscription = subs[0]
            else:
                response.status = 0

        if isinstance(equipment, AccountEquipment):
            subscriptions: QuerySet = AccountSubscription.objects.filter(equipment=equipment).order_by('-id')
            subscription: AccountSubscription | None = None

            if subscriptions.count():
                subscription = subscriptions[0]

        if subscription is None:
            print(f'Could not find subscription for {user_id}')
            response.status = 0
        else:
            print(f'Found subscription for {user_id} with id {subscription.id}')
            response.status = 2

            if isinstance(subscription.lease_time, int):
                response.reply.add_only('Session-Timeout', str(subscription.lease_time))

            if isinstance(subscription.ipv4_address, str):
                response.reply.add_only('Framed-IP-Address', subscription.ipv4_address)
                response.reply.add_only('Framed-IP-Netmask', '255.255.255.0')

            if isinstance(subscription.ipv4_pool, str):
                response.reply.add_only('Framed-Pool', subscription.ipv4_pool)

            if isinstance(subscription.ipv6_prefix, str):
                response.reply.add_only('Delegated-IPv6-Prefix', subscription.ipv6_prefix)

            if isinstance(subscription.ipv6_pool, str):
                response.reply.add_only('Delegated-IPv6-Prefix-Pool', subscription.ipv6_pool)

            if isinstance(subscription.routes, str):
                response.reply.add('Framed-Route', subscription.routes)

            if isinstance(subscription.package.downstream, float) \
                    and isinstance(subscription.package.upstream, float):
                limit: str = f'{int(subscription.package.upstream)}/{int(subscription.package.downstream)}'
                response.reply.add_only('Mikrotik-Rate-Limit', limit)

        response.reply.add_only('Acct-Interim-Interval', '15')

    params: dict = {'status': 200, 'content': response.dumps(), 'content_type': 'application/json'}

    return HttpResponse(**params)
