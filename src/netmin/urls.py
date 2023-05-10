from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.web.sitemaps import StaticViewSitemap


sitemaps = {
    'static': StaticViewSitemap(),
}

urlpatterns = [
    # redirect Django admin login to main login page, this might need tro be changed for PDNS-Admin
    path('admin/login/', RedirectView.as_view(pattern_name='account_login')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('accounts/', include('allauth_2fa.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('apps.users.urls')),
    path('', include('apps.web.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('radius/', include('apps.radius.urls')),
    path('settings/', include('apps.settings.urls')),
    path('subscribers/', include('apps.subscribers.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
