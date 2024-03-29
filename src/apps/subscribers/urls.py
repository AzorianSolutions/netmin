from django.urls import path
from apps.subscribers.views import index, subscriptions, equipment, locations

app_name = 'subscribers'
urlpatterns = [
    path('', index.index, name='index'),
    path('add', index.edit, name='accounts_add'),
    path('api/search', index.api_search, name='accounts_api_search'),
    path('import', index.import_subscribers, name='accounts_import_customers'),
    path('<int:id>/edit', index.edit, name='accounts_edit'),
    path('<int:id>/delete', index.delete, name='accounts_delete'),
    path('<int:subscriber_id>/locations/add', locations.edit, name='locations_add'),
    path('<int:subscriber_id>/locations/<int:id>/edit', locations.edit, name='locations_edit'),
    path('<int:subscriber_id>/locations/<int:id>/delete', locations.delete, name='locations_delete'),
    path('<int:subscriber_id>/equipment/add', equipment.edit, name='equipment_add'),
    path('<int:subscriber_id>/equipment/<int:id>/edit', equipment.edit, name='equipment_edit'),
    path('<int:subscriber_id>/equipment/<int:id>/delete', equipment.delete, name='equipment_delete'),
    path('<int:subscriber_id>/subscriptions/add', subscriptions.edit, name='subscriptions_add'),
    path('<int:subscriber_id>/subscriptions/<int:id>/edit', subscriptions.edit, name='subscriptions_edit'),
    path('<int:subscriber_id>/subscriptions/<int:id>/delete', subscriptions.delete, name='subscriptions_delete'),
]
