import os
from django.shortcuts import redirect, render
from django.http import HttpRequest
from apps.subscribers.models import Subscriber, SubscriberEquipment, SubscriberSubscription
from apps.settings.models import ServicePackage

base_uri: str = '/subscribers'
view_directory: str = os.path.join('subscribers', os.path.basename(__file__).split(".")[0].replace('_', '-'))


def edit(request: HttpRequest, subscriber_id: int, id: int | None = None):
    if request.method == 'POST':

        # Scrub lease time
        lease_time = request.POST.get('lease_time')
        if lease_time is not None and str(lease_time).isnumeric():
            lease_time = int(lease_time)
        else:
            lease_time = None

        data: dict = {
            'subscriber_id': subscriber_id,
            'equipment_id': request.POST.get('equipment_id'),
            'package_id': request.POST.get('package_id'),
            'status': request.POST.get('status'),
            'lease_time': lease_time,
            'ipv4_address': request.POST.get('ipv4_address'),
            'ipv4_netmask': request.POST.get('ipv4_netmask'),
            'ipv4_pool': request.POST.get('ipv4_pool'),
            'ipv6_prefix': request.POST.get('ipv6_prefix'),
            'ipv6_pool': request.POST.get('ipv6_pool'),
            'routes': request.POST.get('routes'),
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
        }

        if isinstance(id, int):
            data['id'] = id

        SubscriberSubscription(**data).save()

        return redirect(f'{base_uri}/{subscriber_id}/edit#subscriptions')

    record: SubscriberSubscription

    if id:
        record = SubscriberSubscription.objects.get(pk=id)
    else:
        record = SubscriberSubscription(subscriber_id=subscriber_id, subscriber=Subscriber())

    params: dict = {
        'id': id,
        'subscriber_id': subscriber_id,
        'record': record,
        'equipment': SubscriberEquipment.objects.filter(subscriber_id=subscriber_id),
        'packages': ServicePackage.objects.all(),
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request: HttpRequest, subscriber_id: int, id: int):
    if request.method == 'POST':
        SubscriberSubscription.objects.get(pk=id).delete()
        return redirect(f'{base_uri}/{subscriber_id}/edit#subscriptions')

    params: dict = {
        'id': id,
        'subscriber_id': subscriber_id,
        'record': SubscriberSubscription.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
