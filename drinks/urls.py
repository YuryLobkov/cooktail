from django.urls import path
from .views import (HomeView, DrinksList, DrinksCreate, DrinksDelete, DrinksDetails,
                    IngredientsCreate, InventoryCreate,
                    UserStorageView, UserStorageDelete, UserToolsDelete, UserToolsView,
                    UserDrinksList)

app_name = 'drinks'

urlpatterns = [ 
    path('', HomeView.as_view(), name='home'),
    path('cocktails/', DrinksList.as_view(), name='cocktail_list'),
    path('add_cocktail/', DrinksCreate.as_view(), name='add_cocktail'),
    path('remove_cocktail/<int:pk>', DrinksDelete.as_view(), name='remove_cocktail'),
    path('cocktail/<int:pk>', DrinksDetails.as_view(), name='cocktail_details'),
    path('add_ingredient/', IngredientsCreate.as_view(), name='add_ingredient'),
    path('add_inventory/', InventoryCreate.as_view(), name='add_inventory'),
    path('mystorage/', UserStorageView.as_view(), name='user_storage'),
    path('mytools/', UserToolsView.as_view(), name='user_tools'),
    path('mystorage/<int:pk>/delete/', UserStorageDelete.as_view(), name='storage_delete'),
    path('mytool/<int:pk>/delete/', UserToolsDelete.as_view(), name='tool_delete'),
    path('whatcanimake/', UserDrinksList.as_view(), name='user_cocktails_from_ings'),
]
