from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Cocktail

# Create your views here.

class HomeView(TemplateView):
    template_name = 'drinks/home.html'


class DrinksList(ListView):
    model = Cocktail
    
