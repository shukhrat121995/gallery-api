"""A list of urls of the app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('wallpaper', views.WallpaperViewSet, basename='wallpaper')
router.register('category', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('search', views.ReactInfiniteSearchView.as_view(), name='search'),
    path('contact-us', views.ContactUsView.as_view(), name='contact-us'),
    path('user/', include('user.urls')),
    path('', include(router.urls))
]
