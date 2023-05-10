import os
from django.shortcuts import redirect, render
from django.http import HttpRequest
from apps.subscribers.models import Subscriber, SubscriberLocation

base_uri: str = '/subscribers'
view_directory: str = os.path.join('subscribers', os.path.basename(__file__).split(".")[0].replace('_', '-'))


def edit(request: HttpRequest, subscriber_id: int, id: int | None = None):
    if request.method == 'POST':
        data: dict = {
            'subscriber_id': subscriber_id,
            'label': request.POST.get('label'),
            'type': request.POST.get('type'),
            'address_line1': request.POST.get('address_line1'),
            'address_line2': request.POST.get('address_line2'),
            'address_city': request.POST.get('address_city'),
            'address_state': request.POST.get('address_state'),
            'address_postal_code': request.POST.get('address_postal_code'),
            'address_country': request.POST.get('address_country'),
        }

        if isinstance(id, int):
            data['id'] = id

        SubscriberLocation(**data).save()

        return redirect(f'{base_uri}/{subscriber_id}/edit#locations')

    record: SubscriberLocation

    if id:
        record = SubscriberLocation.objects.get(pk=id)
    else:
        record = SubscriberLocation(subscriber_id=subscriber_id, subscriber=Subscriber())

    params: dict = {
        'id': id,
        'subscriber_id': subscriber_id,
        'record': record,
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request: HttpRequest, subscriber_id: int, id: int):
    if request.method == 'POST':
        SubscriberLocation.objects.get(pk=id).delete()
        return redirect(f'{base_uri}/{subscriber_id}/edit#locations')

    params: dict = {
        'id': id,
        'subscriber_id': subscriber_id,
        'record': SubscriberLocation.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
