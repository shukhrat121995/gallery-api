"""A list of urls of the app"""
from django.urls import path
from . import views

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('search', views.ReactInfiniteSearchView.as_view()),
    path('contact-us', views.ContactUsView.as_view()),
    path('wallpaper/<int:pk>', views.WallpaperApiView.as_view())
]
