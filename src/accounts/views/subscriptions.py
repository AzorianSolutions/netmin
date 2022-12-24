import os
from django.shortcuts import redirect, render
from django.http import HttpRequest
from accounts.models import Account, AccountSubscription

base_uri: str = '/accounts'
view_directory: str = os.path.join('accounts', os.path.basename(__file__).split(".")[0].replace('_', '-'))


def edit(request: HttpRequest, account_id: int, id: int | None = None):
    if request.method == 'POST':
        data: dict = {
            'account_id': account_id,
            'equipment_id': request.POST.get('equipment_id'),
            'package_id': request.POST.get('package_id'),
            'status': request.POST.get('status'),
            'lease_time': request.POST.get('lease_time'),
            'ipv4_address': request.POST.get('ipv4_address'),
            'ipv4_pool': request.POST.get('ipv4_pool'),
            'ipv6_prefix': request.POST.get('ipv6_prefix'),
            'ipv6_pool': request.POST.get('ipv6_pool'),
            'routes': request.POST.get('routes'),
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
        }

        if isinstance(id, int):
            data['id'] = id

        AccountSubscription(**data).save()

        return redirect(f'{base_uri}/{account_id}/edit#subscriptions')

    record: AccountSubscription

    if id:
        record = AccountSubscription.objects.get(pk=id)
    else:
        record = AccountSubscription(account_id=account_id, account=Account())

    params: dict = {
        'id': id,
        'account_id': account_id,
        'record': record,
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request: HttpRequest, account_id: int, id: int):
    if request.method == 'POST':
        AccountSubscription.objects.get(pk=id).delete()
        return redirect(f'{base_uri}/{account_id}/edit#subscriptions')

    params: dict = {
        'id': id,
        'account_id': account_id,
        'record': AccountSubscription.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
