import hashlib
from django.http import HttpRequest, HttpResponse
from radius.mutables import NetminRequest, NetminResponse


def action_handler(req: HttpRequest, action: str = None):
    print(f'RADIUS Action: {action}')
    print('This action is not currently being handled.')
    request: NetminRequest = NetminRequest.loads(req.body.decode('UTF-8'))
    print(request.json())
    return HttpResponse(status=204)


def authenticate(req: HttpRequest):
    from django.db.models import QuerySet
    from accounts.models import AccountEquipment, AccountSubscription

    print(f'RADIUS Action: authenticate')

    # This map determines what combinations of attributes must be present for each authentication type.
    key_map: dict = {
        'dhcp': ['User-Name', 'Agent-Remote-Id'],
        'ppp-chap': ['User-Name', 'CHAP-Challenge', 'CHAP-Password'],
        'ppp-pap': ['User-Name', 'User-Password'],
    }
    auth_type: str | None = None
    request: NetminRequest = NetminRequest.loads(req.body.decode('UTF-8'))
    response: NetminResponse = NetminResponse()
    pass_statuses: list = [2, 3, 7, 8]

    # Determine the authentication type for the request
    for key, value in key_map.items():
        valid: bool = True
        for item in value:
            if not request.request.has(item):
                valid = False
                break
        if valid:
            auth_type = key
            break

    # Set a failure status if we don't know the authentication type
    if auth_type is None:
        response.status = 4

    # Proceed to handle authentication if the current response status is still passing
    if response.status in pass_statuses:
        user_id: str | None = None
        equipment: AccountEquipment | None = None
        subscription: AccountSubscription | None = None

        # Handle DHCP authentication
        if auth_type == 'dhcp':
            user_id: str = request.request.get_first('Agent-Remote-Id').upper().split('X')[1]
            cpe_id: str = request.request.get_first('User-Name').upper().replace(':', '')

            registrations: QuerySet = AccountEquipment.objects.filter(mac_address=cpe_id)
            if not registrations.count():
                registrations = AccountEquipment.objects.filter(mac_address=user_id)

            if registrations.count():
                equipment = registrations[0]

        # Handle PPPoE CHAP authentication
        if auth_type == 'ppp-chap':
            user_id: str = request.request.get_first('User-Name')
            chap_id: str = request.request.get_first('CHAP-Password')[2:4]
            chap_password: str = request.request.get_first('CHAP-Password')[4:]
            chap_challenge: str = request.request.get_first('CHAP-Challenge')[2:]

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

        # Handle PPPoE PAP authentication
        if auth_type == 'ppp-pap':
            user_id: str = request.request.get_first('User-Name')
            user_password: str = request.request.get_first('User-Password')
            subs: QuerySet = AccountSubscription.objects.filter(username=user_id, password=user_password) \
                .order_by('-id')
            if subs.count():
                subscription = subs[0]
            else:
                response.status = 0

        # Lookup subscription based on known equipment
        if subscription is None and isinstance(equipment, AccountEquipment):
            subscriptions: QuerySet = AccountSubscription.objects.filter(equipment=equipment).order_by('-id')
            subscription: AccountSubscription | None = None

            if subscriptions.count():
                subscription = subscriptions[0]

        # Set the response status to reject if we don't have a subscription
        if subscription is None:
            response.status = 0

        # Proceed to build the response if the current response status is still passing and we have a subscription
        if isinstance(subscription, AccountSubscription) and response.status in pass_statuses:
            response.status = 2

            # DHCP Lease Time / PPPoE Session Timeout
            if isinstance(subscription.lease_time, int):
                response.reply.add_only('Session-Timeout', str(subscription.lease_time))

            # Static IP Address
            if isinstance(subscription.ipv4_address, str):
                response.reply.add_only('Framed-IP-Address', subscription.ipv4_address)
                response.reply.add_only('Framed-IP-Netmask', '255.255.255.0')

            # Static IPv4 Address Pool
            if isinstance(subscription.ipv4_pool, str):
                response.reply.add_only('Framed-Pool', subscription.ipv4_pool)

            # Static IPv6 Prefix
            if isinstance(subscription.ipv6_prefix, str):
                response.reply.add_only('Delegated-IPv6-Prefix', subscription.ipv6_prefix)

            # Static IPv6 Prefix Pool
            if isinstance(subscription.ipv6_pool, str):
                response.reply.add_only('Delegated-IPv6-Prefix-Pool', subscription.ipv6_pool)

            # Static Network Routes
            if isinstance(subscription.routes, str):
                routes: list = subscription.routes.replace('\r', ',').replace('\n', ',').split(',')
                for route in routes:
                    if not len(str(route).strip()):
                        continue
                    response.reply.add('Framed-Route', route)

            # Package Throughput Limit
            if isinstance(subscription.package.downstream, float) \
                    and isinstance(subscription.package.upstream, float):
                limit: str = f'{int(subscription.package.upstream)}/{int(subscription.package.downstream)}'
                response.reply.add_only('Mikrotik-Rate-Limit', limit)

        # Accounting Interval
        response.reply.add_only('Acct-Interim-Interval', '15')

    return HttpResponse(status=200, content=response.dumps(), content_type='application/json')
