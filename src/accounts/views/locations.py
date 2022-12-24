import os
from django.shortcuts import redirect, render
from django.http import HttpRequest

base_uri: str = '/accounts'
view_directory: str = os.path.join('accounts', os.path.basename(__file__).split(".")[0].replace('_', '-'))


def edit(request: HttpRequest, account_id: int, id: int | None = None):
    from accounts.models import Account, AccountLocation

    if request.method == 'POST':
        data: dict = {
            'account_id': account_id,
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

        AccountLocation(**data).save()

        return redirect(f'{base_uri}/{account_id}/edit')

    record: AccountLocation

    if id:
        record = AccountLocation.objects.get(pk=id)
    else:
        record = AccountLocation(account_id=account_id, account=Account())

    params: dict = {
        'id': id,
        'account_id': account_id,
        'record': record,
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request: HttpRequest, account_id: int, id: int):
    from accounts.models import AccountLocation

    if request.method == 'POST':
        AccountLocation.objects.get(pk=id).delete()
        return redirect(base_uri)

    params: dict = {
        'id': id,
        'account_id': account_id,
        'record': AccountLocation.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
