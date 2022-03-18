""" Project url file
This file contains admin and app urls
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('forceartsapi.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
