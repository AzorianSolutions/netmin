import os
import re
from django.shortcuts import redirect, render
from django.http import HttpRequest, JsonResponse
from accounts.models import Account, AccountSubscription, AccountEquipment, AccountLocation
from settings.models import ServicePackage

base_uri: str = '/accounts'
view_directory: str = 'accounts'
numbers_regex = re.compile(r'\d+')
package_regex = re.compile(
    r'([0-9]{1,4}(?:\.[0-9]{1,3})?)[:space:]*(k|m|g){1}(?:b|bps|bsp|sbp|pbs|spb)?/([0-9]{1,4}(?:\.[0-9]{1,3})?)[:space:]*(k|m|g){1}(?:b|bps|bsp|sbp|pbs|spb)?')


def import_accounts(request: HttpRequest):
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
        account_props: dict = {
            'org_name': '',
            'primary_contact_name': '',
            'primary_contact_phone1': '',
            'secondary_contact_name': '',
            'secondary_contact_phone1': '',
        }
        is_commercial: bool = False

        if 'billing_address' in customer and 'line1' in customer['billing_address'] \
                and customer['billing_address']['line1'] == customer['full_name']:
            account_props['org_name'] = customer['full_name']

        if 'contact' in customer:
            account_props['primary_contact_name'] = customer['contact']
        elif 'first_name' in customer and 'last_name' in customer:
            account_props['primary_contact_name'] = customer['first_name'] + ' ' + customer['last_name']

        if 'alt_contact' in customer:
            account_props['secondary_contact_name'] = customer['alt_contact']

        if 'phone' in customer:
            account_props['primary_contact_phone1'] = re.sub(r'[^0-9]', '', customer['phone'])

        if 'alt_phone' in customer:
            account_props['secondary_contact_phone1'] = re.sub(r'[^0-9]', '', customer['alt_phone'])

        if len(account_props['org_name']):
            is_commercial = True

        account = Account(**account_props)
        account.save()

        if 'billing_address' in customer:
            location_props: dict = {
                'account': account,
                'label': 'Home' if not is_commercial else 'Office',
                'type': 'residential' if not is_commercial else 'commercial',
                'address_line1': customer['billing_address']['line2'],
                'address_city': customer['billing_address']['city'],
                'address_state': customer['billing_address']['state'],
                'address_postal_code': customer['billing_address']['postal_code'],
                'address_country': 'US',
            }

            location = AccountLocation(**location_props)
            location.save()

        equipment_props: dict = {
            'account': account,
            'location': location or None,
            'label': 'Service Radio',
            'type': 'bridge',
            'mac_address': 'FF:FF:FF:FF:FF:FF',
            'serial_number': 'FFFFFFFFFF',
        }

        equipment = AccountEquipment(**equipment_props)
        equipment.save()

        customers[customer['id']] = {
            'qb': customer,
            'account': account,
            'location': location,
            'equipment': equipment,
        }

    for invoice in qb_invoices:
        customer_id: str = invoice['parent_id']['ListID']

        if customer_id not in customers:
            print('Skipping customer not cached in customers: ' + customer_id)
            continue

        customer: dict = customers[customer_id]['qb']
        account: Account = customers[customer_id]['account']
        location: AccountLocation = customers[customer_id]['location']
        equipment: AccountEquipment = customers[customer_id]['equipment']

        if 'items' not in invoice:
            print('Skipping invoice without items: ' + invoice['id'])
            continue

        for item in invoice['items']:
            # Skip non-internet service items
            if 'item_id' not in item or 'FullName' not in item['item_id'] \
                    and not item['item_id']['FullName'].startswith('WirelessBB'):
                #print('Skipping item: ' + item['description'])
                continue

            label: str = item['description']
            match = re.search(package_regex, label)

            if match is None or len(match.groups()) < 4:
                print('Skipping unmatched item: ' + label)
                continue

            downstream: float = float(match.group(1))
            upstream: float = float(match.group(3))

            if match.group(2).lower() == 'k':
                downstream *= 1000

            if match.group(4).lower() == 'k':
                upstream *= 1000

            if match.group(2).lower() == 'm':
                downstream *= 1000000

            if match.group(4).lower() == 'm':
                upstream *= 1000000

            if match.group(2).lower() == 'g':
                downstream *= 1000000000

            if match.group(4).lower() == 'g':
                upstream *= 1000000000

            throughput_buffer: int = 5000000

            package = ServicePackage.objects.filter(
                downstream__gte=downstream - throughput_buffer,
                downstream__lte=downstream + throughput_buffer,
                upstream__gte=upstream - throughput_buffer,
                upstream__lte=upstream + throughput_buffer,
            ).first()

            if package is None:
                print(f'Skipping unmatched package: {downstream / 1000000} Mbps / {upstream / 1000000} Mbps')
                continue

            subscription_props: dict = {
                'account': account,
                'equipment': equipment,
                'package': package,
                'status': 'active',
                'username': '',
                'password': '',
            }
            subscription = AccountSubscription(**subscription_props)
            subscription.save()

            print('Saved subscription: ' + customer_id)

    return JsonResponse(response)


def index(request: HttpRequest):
    params: dict = {
        'records': Account.objects.all().order_by('primary_contact_name', 'secondary_contact_name', 'org_name'),
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


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

        Account(**data).save()

        return redirect(base_uri)

    params: dict = {
        'id': id,
        'record': Account.objects.get(pk=id) if id else Account(),
        'locations': AccountLocation.objects.filter(account_id=id),
        'equipment': AccountEquipment.objects.filter(account_id=id),
        'subscriptions': AccountSubscription.objects.filter(account_id=id),
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request, id: int):
    if request.method == 'POST':
        Account.objects.get(pk=id).delete()
        return redirect(base_uri)

    params: dict = {
        'id': id,
        'record': Account.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
