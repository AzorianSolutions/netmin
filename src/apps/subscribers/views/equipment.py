import os
import re
from django.shortcuts import redirect, render
from django.http import HttpRequest
from apps.subscribers.models import Subscriber, SubscriberLocation, SubscriberEquipment

base_uri: str = '/subscribers'
view_directory: str = os.path.join('subscribers', os.path.basename(__file__).split(".")[0].replace('_', '-'))
mac_address_regex = re.compile(f'[a-fA-F0-9]')

def edit(request: HttpRequest, subscriber_id: int, id: int | None = None):
    if request.method == 'POST':
        data: dict = {
            'subscriber_id': subscriber_id,
            'location_id': request.POST.get('location_id'),
            'label': request.POST.get('label'),
            'type': request.POST.get('type'),
            'mac_address': ''.join(mac_address_regex.findall(request.POST.get('mac_address'))).upper(),
            'serial_number': request.POST.get('serial_number'),
        }

        if isinstance(id, int):
            data['id'] = id

        SubscriberEquipment(**data).save()

        return redirect(f'{base_uri}/{subscriber_id}/edit#equipment')

    record: SubscriberEquipment

    if id:
        record = SubscriberEquipment.objects.get(pk=id)
    else:
        record = SubscriberEquipment(subscriber_id=subscriber_id, subscriber=Subscriber())

    params: dict = {
        'id': id,
        'subscriber_id': subscriber_id,
        'record': record,
        'locations': SubscriberLocation.objects.filter(subscriber_id=subscriber_id),
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request: HttpRequest, subscriber_id: int, id: int):
    if request.method == 'POST':
        SubscriberEquipment.objects.get(pk=id).delete()
        return redirect(f'{base_uri}/{subscriber_id}/edit#equipment')

    params: dict = {
        'id': id,
        'subscriber_id': subscriber_id,
        'record': SubscriberEquipment.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
