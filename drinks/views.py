from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, 
                                CreateView, DeleteView,
                                DetailView)
from .models import Cocktail, Ingredients, Inventory
from django.urls import reverse_lazy

# Create your views here.

class HomeView(TemplateView):
    template_name = 'drinks/home.html'


class DrinksList(ListView):
    model = Cocktail


class DrinksCreate(CreateView):
    model = Cocktail
    fields = '__all__'
    success_url = reverse_lazy('drinks:cocktail_list')


class DrinksDelete(DeleteView):
    model = Cocktail
    success_url = reverse_lazy('drinks:cocktail_list')


class DrinksDetails(DetailView):
    model = Cocktail


class IngredientsList(ListView):
    model = Ingredients


class IngredientsCreate(CreateView):
    model = Ingredients
    fields = '__all__'
    success_url = reverse_lazy('drinks:ingredients')


class InventoryList(ListView):
    model = Inventory


class InventoryCreate(CreateView):
    model = Inventory
    fields = '__all__'
    success_url = reverse_lazy('drinks:inventory_list')
