from django.urls import path
from accounts.views import index

app_name = 'accounts'
urlpatterns = [
    path('', index.index, name='index'),
    path('add', index.edit, name='accounts_add'),
    path('<int:id>/edit', index.edit, name='accounts_edit'),
    path('<int:id>/delete', index.delete, name='accounts_delete'),
]
