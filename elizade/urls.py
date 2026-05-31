from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

# Secret admin URL — read from .env
ADMIN_URL = config('ADMIN_URL', default='elizade-admin-2026/')

# Customise admin panel branding
admin.site.site_header  = 'Elizade Motors Admin'
admin.site.site_title   = 'Elizade Admin Portal'
admin.site.index_title  = 'Inventory Management'



urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path('', include('home.app_urls')),
]
# Serve media files in development only
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )