from django.urls import path
from .views import HomeView, DrinksList, DrinksCreate, DrinksDelete, DrinksDetails, IngredientsList, IngredientsCreate, InventoryList, InventoryCreate

app_name = 'drinks'

urlpatterns = [ 
    path('', HomeView.as_view(), name='home'),
    path('cocktails/', DrinksList.as_view(), name='cocktail_list'),
    path('add_cocktail/', DrinksCreate.as_view(), name='add_cocktail'),
    path('remove_cocktail/<int:pk>', DrinksDelete.as_view(), name='remove_cocktail'),
    path('cocktail/<int:pk>', DrinksDetails.as_view(), name='cocktail_details'),
    path('ingredients/', IngredientsList.as_view(), name='ingredients'),
    path('add_ingredient/', IngredientsCreate.as_view(), name='add_ingredient'),
    path('inventory/', InventoryList.as_view(), name='inventory_list'),
    path('add_inventory/', InventoryCreate.as_view(), name='add_inventory'),
]
