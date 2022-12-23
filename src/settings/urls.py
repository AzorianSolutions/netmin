from django.urls import path
from settings.views import equipment_configurations, index, service_packages

app_name = 'settings'
urlpatterns = [
    path('', index.index, name='index'),
    path('equipment-configurations/', equipment_configurations.index, name='equipment_configurations_index'),
    path('equipment-configurations/add', equipment_configurations.edit, name='equipment_configurations_add'),
    path('equipment-configurations/<int:id>/edit', equipment_configurations.edit, name='equipment_configurations_edit'),
    path('equipment-configurations/<int:id>/delete', equipment_configurations.delete,
         name='equipment_configurations_delete'),
    path('service-packages/', service_packages.index, name='service_packages_index'),
    path('service-packages/add', service_packages.add, name='service_packages_add'),
    path('service-packages/<int:id>/edit', service_packages.edit, name='service_packages_edit'),
    path('service-packages/<int:id>/delete', service_packages.delete, name='service_packages_delete'),
]
