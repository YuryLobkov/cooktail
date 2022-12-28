from django.urls import path
from .views import HomeView, DrinksList, DrinksCreate, DrinksDelete, DrinksDetails

app_name = 'drinks'

urlpatterns = [ 
    path('', HomeView.as_view(), name='home'),
    path('cocktails/', DrinksList.as_view(), name='cocktail_list'),
    path('add_cocktail/', DrinksCreate.as_view(), name='add_cocktail'),
    path('remove_cocktail/<int:pk>', DrinksDelete.as_view(), name='remove_cocktail'),
    path('cocktail/<int:pk>', DrinksDetails.as_view(), name='cocktail_details'),
]
