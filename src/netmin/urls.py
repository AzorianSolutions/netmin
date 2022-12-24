from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('', include('dashboard.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('settings/', include('settings.urls')),
    path('admin/', admin.site.urls),
]
