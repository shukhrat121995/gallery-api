"""A list of urls of the app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('wallpaper', views.WallpaperViewSet, basename='wallpaper')

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('search', views.ReactInfiniteSearchView.as_view()),
    path('contact-us', views.ContactUsView.as_view()),
    path('', include(router.urls))
]
