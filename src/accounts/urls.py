from django.urls import path
from accounts.views import index, locations, equipment, subscriptions

app_name = 'accounts'
urlpatterns = [
    path('', index.index, name='index'),
    path('add', index.edit, name='accounts_add'),
    path('<int:id>/edit', index.edit, name='accounts_edit'),
    path('<int:id>/delete', index.delete, name='accounts_delete'),
    path('<int:account_id>/locations/add', locations.edit, name='locations_add'),
    path('<int:account_id>/locations/<int:id>/edit', locations.edit, name='locations_edit'),
    path('<int:account_id>/locations/<int:id>/delete', locations.delete, name='locations_delete'),
    path('<int:account_id>/equipment/add', equipment.edit, name='equipment_add'),
    path('<int:account_id>/equipment/<int:id>/edit', equipment.edit, name='equipment_edit'),
    path('<int:account_id>/equipment/<int:id>/delete', equipment.delete, name='equipment_delete'),
    path('<int:account_id>/subscriptions/add', subscriptions.edit, name='subscriptions_add'),
    path('<int:account_id>/subscriptions/<int:id>/edit', subscriptions.edit, name='subscriptions_edit'),
    path('<int:account_id>/subscriptions/<int:id>/delete', subscriptions.delete, name='subscriptions_delete'),
]
