from django.urls import path
from . import views

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('characters', views.CharactersView.as_view()),
    path('search', views.ReactInfiniteSearchView.as_view()),
    path('contact-us', views.ContactUsView.as_view()),
    path('increment-views/<int:pk>', views.increment_views),
    path('likes/<int:pk>/<str:value>', views.inc_dec_likes)
]