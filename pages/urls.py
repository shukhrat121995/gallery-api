from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('characters', views.characters, name='characters'),
    path('contact', views.contact, name='contact'),
    path('license', views.license, name='license'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
