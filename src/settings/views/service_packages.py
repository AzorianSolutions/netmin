import os
from django.shortcuts import render
from django.http import HttpRequest

base_uri: str = '/settings/service-packages'
view_directory: str = os.path.join('settings', os.path.basename(__file__).split(".")[0])
unlimited_mark: str = '~'


def index(request: HttpRequest):
    from settings.models import ServicePackage

    params: dict = {
        'packages': ServicePackage.objects.all().order_by('label', 'type', 'technologies', 'downstream', 'upstream'),
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


def add(request: HttpRequest):
    from django.shortcuts import redirect
    from settings.models import ServicePackage

    if request.method == 'POST':
        technologies: list | str | None = request.POST.getlist('technologies')
        downstream: float | str | None = request.POST.get('downstream')
        upstream: float | str | None = request.POST.get('upstream')

        if isinstance(technologies, list):
            technologies = ','.join(technologies)

        try:
            downstream = float(downstream)
            downstream = downstream * 1000000 if downstream > 0 else 0
        except ValueError:
            downstream = 0

        try:
            upstream = float(upstream)
            upstream = upstream * 1000000 if upstream > 0 else 0
        except ValueError:
            upstream = 0

        data: dict = {
            'label': request.POST.get('label'),
            'technologies': technologies,
            'type': request.POST.get('type'),
            'downstream': downstream,
            'upstream': upstream,
        }
        package = ServicePackage(**data)
        package.save()

        return redirect(base_uri)

    package: ServicePackage = ServicePackage()

    try:
        if package.downstream is not None:
            package.downstream = float(package.downstream) / 1000000
        if not package.downstream:
            package.downstream = unlimited_mark
    except ValueError:
        package.downstream = unlimited_mark

    try:
        if package.upstream is not None:
            package.upstream = float(package.upstream) / 1000000
        if not package.upstream:
            package.upstream = unlimited_mark
    except ValueError:
        package.upstream = unlimited_mark

    params: dict = {
        'id': None,
        'package': package,
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def edit(request, id):
    from django.shortcuts import redirect
    from settings.models import ServicePackage

    if request.method == 'POST':
        technologies: list | str | None = request.POST.getlist('technologies')
        downstream: float | str | None = request.POST.get('downstream')
        upstream: float | str | None = request.POST.get('upstream')

        if isinstance(technologies, list):
            technologies = ','.join(technologies)

        try:
            downstream = float(downstream)
            downstream = downstream * 1000000 if downstream > 0 else 0
        except ValueError:
            downstream = 0

        try:
            upstream = float(upstream)
            upstream = upstream * 1000000 if upstream > 0 else 0
        except ValueError:
            upstream = 0

        data: dict = {
            'id': id,
            'label': request.POST.get('label'),
            'technologies': technologies,
            'type': request.POST.get('type'),
            'downstream': downstream,
            'upstream': upstream,
        }
        package = ServicePackage(**data)
        package.save()

        return redirect(base_uri)

    package: ServicePackage = ServicePackage.objects.get(pk=id)

    try:
        if package.downstream is not None:
            package.downstream = float(package.downstream) / 1000000
        if not package.downstream:
            package.downstream = unlimited_mark
    except ValueError:
        package.downstream = unlimited_mark

    try:
        if package.upstream is not None:
            package.upstream = float(package.upstream) / 1000000
        if not package.upstream:
            package.upstream = unlimited_mark
    except ValueError:
        package.upstream = unlimited_mark

    params: dict = {
        'id': id,
        'package': package,
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request, id):
    from django.shortcuts import redirect
    from settings.models import ServicePackage

    if request.method == 'POST':
        ServicePackage.objects.get(pk=id).delete()

        return redirect(base_uri)

    params: dict = {
        'id': id,
        'package': ServicePackage.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)