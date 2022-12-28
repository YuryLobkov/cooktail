from django.urls import path
from .views import HomeView, DrinksList, DrinksCreate

app_name = 'drinks'

urlpatterns = [ 
    path('', HomeView.as_view(), name='home'),
    path('cocktails/', DrinksList.as_view(), name='cocktail_list'),
    path('add_cocktail/', DrinksCreate.as_view(), name='add_cocktail'),
]
