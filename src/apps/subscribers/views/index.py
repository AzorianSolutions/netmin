import os
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, JsonResponse
from lib.api.search import SearchApi, SearchConfig
from apps.subscribers.models import Subscriber, SubscriberSubscription, SubscriberEquipment, SubscriberLocation
from apps.settings.models import ServicePackage

base_uri: str = '/subscribers'
view_directory: str = 'subscribers'
numbers_regex = re.compile(r'\d+')
package_regex = re.compile(
    r'([0-9]{1,4}(?:\.[0-9]{1,3})?)[:space:]*(k|m|g){1}(?:b|bps|bsp|sbp|pbs|spb)?/([0-9]{1,4}(?:\.[0-9]{1,'
    r'3})?)[:space:]*(k|m|g){1}(?:b|bps|bsp|sbp|pbs|spb)?')
package_map: dict[str, dict[str, tuple]] = {
    '1.5': {
      '512.0': (1750000, 350000),
    },
    '2.0': {
        '768.0': (2120000, 424000),
    },
    '3.0': {
        '1.0': (3120000, 624000),
    },
    '5.0': {
        '1.0': (5500000, 1120000),
    },
    '6.0': {
        '2.0': (6500000, 1300000),
    },
    '10.0': {
        '2.0': (11500000, 2300000),
    },
    '15.0': {
        '2.0': (16000000, 3000000),
        '3.0': (16000000, 3000000),
    },
    '20.0': {
        '2.0': (24500000, 4900000),
        '5.0': (24500000, 4900000),
        '10.0': (24500000, 10000000),
        '15.0': (24500000, 15000000),
    },
    '24.5': {
        '10': (25000000, 10000000),
    },
    '25.0': {
        '10.0': (25000000, 10000000),
    },
    '30.0': {
        '6.0': (31000000, 6000000),
    },
    '40.0': {
        '6.0': (42500000, 8500000),
    },
    '50.0': {
        '10.0': (51000000, 10000000),
    },
    '75.0': {
        '12.0': (76000000, 15000000),
        '15.0': (76000000, 15000000),
    },
    '100.0': {
        '100.0': (100000000, 100000000),
    },
}


@login_required
def index(request: HttpRequest):
    params: dict = {}
    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


@login_required
def api_search(request: HttpRequest):
    # Deny any requests that aren't using the POST HTTP verb
    if request.method != 'POST':
        return HttpResponse(status=405)

    columns: list = ['id', 'primary_contact_name', 'secondary_contact_name', 'org_name', 'notes']

    # Configure the search operation
    config: SearchConfig = SearchConfig()
    config.columns = columns
    config.params = request.POST

    # Execute the search operation and return the results as JSON for DataTables
    return SearchApi.search_json(Subscriber, config)


@login_required
def edit(request, id: int | None = None):
    if request.method == 'POST':
        phone_fields: list = [
            'primary_contact_phone1',
            'primary_contact_phone2',
            'secondary_contact_phone1',
            'secondary_contact_phone2',
        ]

        data: dict = {
            'org_name': request.POST.get('org_name'),
            'primary_contact_name': request.POST.get('primary_contact_name'),
            'secondary_contact_name': request.POST.get('secondary_contact_name'),
            'notes': request.POST.get('notes'),
        }

        for field in phone_fields:
            if not (field_value := request.POST.get(field)):
                continue

            result: str = ''.join(numbers_regex.findall(field_value))

            if len(result.strip()) and result.isnumeric():
                data[field] = int(result)

        if isinstance(id, int):
            data['id'] = id

        Subscriber(**data).save()

        return redirect(base_uri)

    params: dict = {
        'id': id,
        'record': Subscriber.objects.get(pk=id) if id else Subscriber(),
        'locations': SubscriberLocation.objects.filter(subscriber_id=id),
        'equipment': SubscriberEquipment.objects.filter(subscriber_id=id),
        'subscriptions': SubscriberSubscription.objects.filter(subscriber_id=id),
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


@login_required
def delete(request, id: int):
    if request.method == 'POST':
        Subscriber.objects.get(pk=id).delete()
        return redirect(base_uri)

    params: dict = {
        'id': id,
        'record': Subscriber.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)


@login_required
def import_subscribers(request: HttpRequest):
    import json

    response: dict = {
        'status': 1,
        'messages': [],
        'payload': {},
    }

    qb_customers_path: str = 'var/customers.json'
    qb_invoices_path: str = 'var/invoices.json'
    customers: dict = {}

    with open(qb_customers_path, 'r') as f:
        qb_customers: dict = json.load(f)
        f.close()

    with open(qb_invoices_path, 'r') as f:
        qb_invoices: dict = json.load(f)
        f.close()

    for customer in qb_customers:
        subscriber_props: dict = {
            'org_name': '',
            'primary_contact_name': '',
            'primary_contact_phone1': '',
            'secondary_contact_name': '',
            'secondary_contact_phone1': '',
        }
        is_commercial: bool = False

        if 'billing_address' in customer and 'line1' in customer['billing_address'] \
                and customer['billing_address']['line1'] == customer['full_name']:
            subscriber_props['org_name'] = customer['full_name']

        if 'contact' in customer:
            subscriber_props['primary_contact_name'] = customer['contact']
        elif 'first_name' in customer and 'last_name' in customer:
            subscriber_props['primary_contact_name'] = customer['first_name'] + ' ' + customer['last_name']

        if 'alt_contact' in customer:
            subscriber_props['secondary_contact_name'] = customer['alt_contact']

        if 'phone' in customer:
            subscriber_props['primary_contact_phone1'] = re.sub(r'[^0-9]', '', customer['phone'])

        if 'alt_phone' in customer:
            subscriber_props['secondary_contact_phone1'] = re.sub(r'[^0-9]', '', customer['alt_phone'])

        if len(subscriber_props['org_name']):
            is_commercial = True

        subscriber = Subscriber(**subscriber_props)
        subscriber.save()

        location = None
        if 'billing_address' in customer:
            location_props: dict = {
                'subscriber': subscriber,
                'label': 'Home' if not is_commercial else 'Office',
                'type': 'residential' if not is_commercial else 'commercial',
                'address_line1': customer['billing_address']['line2'],
                'address_city': customer['billing_address']['city'],
                'address_state': customer['billing_address']['state'],
                'address_postal_code': customer['billing_address']['postal_code'],
                'address_country': 'US',
            }

            location = SubscriberLocation(**location_props)
            location.save()

        if location is None:
            print('Skipping customer without billing address: ' + customer['id'])
            continue

        equipment_props: dict = {
            'subscriber': subscriber,
            'location': location,
            'label': 'Service Radio',
            'type': 'bridge',
            'mac_address': 'FFFFFFFFFFFF',
            'serial_number': 'FFFFFFFFFF',
        }

        equipment = SubscriberEquipment(**equipment_props)
        equipment.save()

        customers[customer['id']] = {
            'qb': customer,
            'subscriber': subscriber,
            'location': location,
            'equipment': equipment,
        }

    for invoice in qb_invoices:
        customer_id: str = invoice['parent_id']['ListID']

        if customer_id not in customers:
            print('Skipping customer not cached in customers: ' + customer_id)
            continue

        customer: dict = customers[customer_id]['qb']
        subscriber: Subscriber = customers[customer_id]['subscriber']
        location: SubscriberLocation = customers[customer_id]['location']
        equipment: SubscriberEquipment = customers[customer_id]['equipment']

        if 'items' not in invoice:
            print('Skipping invoice without items: ' + invoice['id'])
            continue

        for item in invoice['items']:
            # Skip non-internet service items
            if 'item_id' not in item or 'FullName' not in item['item_id'] \
                    and not item['item_id']['FullName'].startswith('WirelessBB'):
                # print('Skipping item: ' + item['description'])
                continue

            label: str = item['description']
            match = re.search(package_regex, label)

            if match is None or len(match.groups()) < 4:
                # print('Skipping unmatched item: ' + label)
                continue

            downstream: str = str(float(match.group(1)))
            upstream: str = str(float(match.group(3)))

            if downstream not in package_map or upstream not in package_map[downstream]:
                print('Skipping unmatched package: ' + label)
                continue

            query_params: tuple = package_map[downstream][upstream]

            package = ServicePackage.objects.filter(
                downstream=query_params[0],
                upstream=query_params[1],
            ).first()

            if package is None:
                print(f'Skipping unmatched package: {query_params[0] / 1000000} Mbps / {query_params[1] / 1000000} Mbps')
                continue

            subscription_props: dict = {
                'subscriber': subscriber,
                'equipment': equipment,
                'package': package,
                'status': 'active',
                'username': '',
                'password': '',
            }
            subscription = SubscriberSubscription(**subscription_props)
            subscription.save()

            # print('Saved subscription: ' + customer_id)

    return JsonResponse(response)
