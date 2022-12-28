from django.urls import path
from .views import HomeView, DrinksList

app_name = 'drinks'

urlpatterns = [ 
    path('', HomeView.as_view(), name='home'),
    path('cocktails/', DrinksList.as_view(), name='Cocktai_list'),
]
