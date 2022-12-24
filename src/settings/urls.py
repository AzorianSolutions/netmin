from django.urls import path
from settings.views import index, service_packages

app_name = 'settings'
urlpatterns = [
    path('', index.index, name='index'),
    path('service-packages/', service_packages.index, name='service_packages_index'),
    path('service-packages/add', service_packages.edit, name='service_packages_add'),
    path('service-packages/<int:id>/edit', service_packages.edit, name='service_packages_edit'),
    path('service-packages/<int:id>/delete', service_packages.delete, name='service_packages_delete'),
]
