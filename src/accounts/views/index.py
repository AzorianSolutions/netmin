import os
import re
from django.shortcuts import redirect, render
from django.http import HttpRequest

base_uri: str = '/accounts'
view_directory: str = 'accounts'
numbers_regex = re.compile(r'\d+')


def index(request: HttpRequest):
    from accounts.models import Account

    params: dict = {
        'records': Account.objects.all().order_by('primary_contact_name', 'secondary_contact_name', 'org_name',
                                                  'notes'),
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


def edit(request, id: int | None = None):
    from accounts.models import Account, AccountSubscription, AccountEquipment, AccountLocation

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
    from accounts.models import Account

    if request.method == 'POST':
        Account.objects.get(pk=id).delete()
        return redirect(base_uri)

    params: dict = {
        'id': id,
        'account': Account.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
