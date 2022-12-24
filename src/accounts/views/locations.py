import os
from django.shortcuts import render
from django.http import HttpRequest

view_directory: str = os.path.join('accounts', os.path.basename(__file__).split(".")[0])


def edit(request: HttpRequest, account_id: int, id: int | None = None):
    from accounts.models import AccountLocation

    params: dict = {
        'id': id,
        'account_id': account_id,
        'record': AccountLocation.objects.get(pk=id) if id else AccountLocation(),
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request: HttpRequest, account_id: int, id: int):
    from accounts.models import AccountLocation

    params: dict = {
        'id': id,
        'account_id': account_id,
        'record': AccountLocation.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
