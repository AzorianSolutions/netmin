import os
import re
from django.shortcuts import redirect, render
from django.http import HttpRequest
from accounts.models import Account, AccountLocation, AccountEquipment

base_uri: str = '/accounts'
view_directory: str = os.path.join('accounts', os.path.basename(__file__).split(".")[0].replace('_', '-'))
mac_address_regex = re.compile(f'[a-fA-F0-9]')

def edit(request: HttpRequest, account_id: int, id: int | None = None):
    if request.method == 'POST':
        data: dict = {
            'account_id': account_id,
            'location_id': request.POST.get('location_id'),
            'label': request.POST.get('label'),
            'type': request.POST.get('type'),
            'mac_address': ''.join(mac_address_regex.findall(request.POST.get('mac_address'))).upper(),
            'serial_number': request.POST.get('serial_number'),
        }

        if isinstance(id, int):
            data['id'] = id

        AccountEquipment(**data).save()

        return redirect(f'{base_uri}/{account_id}/edit#equipment')

    record: AccountEquipment

    if id:
        record = AccountEquipment.objects.get(pk=id)
    else:
        record = AccountEquipment(account_id=account_id, account=Account())

    params: dict = {
        'id': id,
        'account_id': account_id,
        'record': record,
        'locations': AccountLocation.objects.filter(account_id=account_id),
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request: HttpRequest, account_id: int, id: int):
    if request.method == 'POST':
        AccountEquipment.objects.get(pk=id).delete()
        return redirect(f'{base_uri}/{account_id}/edit#equipment')

    params: dict = {
        'id': id,
        'account_id': account_id,
        'record': AccountEquipment.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
