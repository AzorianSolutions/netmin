import os
from django.shortcuts import render
from django.http import HttpRequest

base_uri: str = '/settings/equipment-configurations'
view_directory: str = os.path.join('settings', os.path.basename(__file__).split(".")[0])


def index(request: HttpRequest):
    from settings.models import EquipmentConfiguration

    params: dict = {
        'configurations': EquipmentConfiguration.objects.all().order_by('label', 'frequency_band'),
        'frequency_bands': EquipmentConfiguration.FREQUENCY_BANDS,
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


def edit(request, id: int | None = None):
    from django.shortcuts import redirect
    from settings.models import EquipmentConfiguration

    if request.method == 'POST':
        internal_gain: int | str | None = request.POST.get('internal_gain')
        external_gain: int | str | None = request.POST.get('external_gain')
        beamwidth: int | str | None = request.POST.get('beamwidth')
        downtilt: int | str | None = request.POST.get('downtilt')

        try:
            internal_gain = int(internal_gain)
            internal_gain = 0 if internal_gain < 0 else internal_gain
        except ValueError:
            internal_gain = 0

        try:
            external_gain = int(external_gain)
            external_gain = 0 if external_gain < 0 else external_gain
        except ValueError:
            external_gain = 0

        try:
            beamwidth = int(beamwidth)
            beamwidth = 0 if beamwidth < 0 else beamwidth
        except ValueError:
            beamwidth = 0

        try:
            downtilt = int(downtilt)
            downtilt = 0 if downtilt < 0 else downtilt
        except ValueError:
            downtilt = 0

        data: dict = {
            'label': request.POST.get('label'),
            'frequency_band': request.POST.get('frequency_band'),
            'internal_gain': internal_gain,
            'external_gain': external_gain,
            'beamwidth': beamwidth,
            'downtilt': downtilt,
        }

        if isinstance(id, int):
            data['id'] = id

        EquipmentConfiguration(**data).save()

        return redirect(base_uri)

    configuration: EquipmentConfiguration

    if isinstance(id, int) and id:
        configuration = EquipmentConfiguration.objects.get(pk=id)
    else:
        configuration = EquipmentConfiguration()

    params: dict = {
        'id': id,
        'configuration': configuration,
        'frequency_bands': EquipmentConfiguration.FREQUENCY_BANDS,
    }

    return render(request, os.path.join(view_directory, 'edit.jinja2'), params)


def delete(request, id: int):
    from django.shortcuts import redirect
    from settings.models import EquipmentConfiguration

    if request.method == 'POST':
        EquipmentConfiguration.objects.get(pk=id).delete()

        return redirect(base_uri)

    params: dict = {
        'id': id,
        'configuration': EquipmentConfiguration.objects.get(pk=id),
    }

    return render(request, os.path.join(view_directory, 'delete.jinja2'), params)
