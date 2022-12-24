from django.db.models import Count, QuerySet
from django.shortcuts import render
from accounts.models import Account, AccountLocation, AccountEquipment, AccountSubscription
from settings.models import ServicePackage


def index(request):
    from django.forms.models import model_to_dict

    subscriptions: QuerySet = AccountSubscription.objects.all()
    total_subscriptions: int = subscriptions.count()
    total_subscriptions_active: int = subscriptions.filter(status='active').count()
    total_subscriptions_canceled: int = subscriptions.filter(status='canceled').count()
    total_subscriptions_paused: int = subscriptions.filter(status='paused').count()
    total_subscriptions_pending: int = subscriptions.filter(status='pending').count()
    total_subscriptions_delinquent: int = subscriptions.filter(status='delinquent').count()
    service_package_map: dict = {}
    service_package_extras: dict = {'total': 0, 'share': 0}

    for r in ServicePackage.objects.order_by('label').all():
        service_package_map[r.pk] = {**model_to_dict(r), **service_package_extras}

    for item in subscriptions.filter(status='active').values('package_id').annotate(total=Count('package_id')):
        service_package_map[item['package_id']]['total'] = item['total']
        service_package_map[item['package_id']]['share'] = item['total'] / total_subscriptions_active * 100

    params: dict = {
        'total_accounts': Account.objects.all().count(),
        'total_locations': AccountLocation.objects.all().count(),
        'total_equipment': AccountEquipment.objects.all().count(),
        'total_subscriptions': total_subscriptions,
        'total_subscriptions_active': total_subscriptions_active,
        'total_subscriptions_canceled': total_subscriptions_canceled,
        'total_subscriptions_paused': total_subscriptions_paused,
        'total_subscriptions_pending': total_subscriptions_pending,
        'total_subscriptions_delinquent': total_subscriptions_delinquent,
        'service_package_map': service_package_map,
    }

    return render(request, 'dashboard/index.jinja2', params)
