from django.urls import path

from . import views

urlpatterns=[
    path('drinks', views.Drinks.as_view()),
    path('drinks/create', views.DrinksCreate.as_view()),
]