import os
import re
from django.shortcuts import render
from django.http import HttpRequest

base_uri: str = '/accounts'
view_directory: str = 'accounts'
numbers_regex = re.compile(r'^\\d+$')


def index(request: HttpRequest):
    from accounts.models import Account

    params: dict = {
        'accounts': Account.objects.all().order_by('primary_contact_name', 'secondary_contact_name', 'org_name',
                                                   'notes'),
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


def edit(request, id: int | None = None):
    from django.shortcuts import redirect
    from accounts.models import Account

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
            result: str = ''.join(numbers_regex.findall(request.POST.get(field)))
            if len(result.strip()) and result.isnumeric():
                data[field] = int(result)

        if isinstance(id, int):
            data['id'] = id

        package = Account(**data)
        package.save()

        return redirect(base_uri)

    account: Account

    if isinstance(id, int) and id:
        account = Account.objects.get(pk=id)
    else:
        account = Account()
        
    params: dict = {
        'id': id,
        'account': account,
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request, id: int):
    from django.shortcuts import redirect
    from accounts.models import Account

    if request.method == 'POST':
        Account.objects.get(pk=id).delete()

        return redirect(base_uri)

    params: dict = {
        'id': id,
        'account': Account.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
