from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, 
                                CreateView, DeleteView,
                                DetailView)
from .models import Cocktail
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
