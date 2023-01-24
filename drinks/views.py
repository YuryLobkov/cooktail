from django.shortcuts import render
from django.views import View
from django.views.generic import (TemplateView, ListView, 
                                CreateView, DeleteView,
                                DetailView, FormView)
from .models import Cocktail, Ingredients, Inventory, UserStorage
from django.urls import reverse_lazy, reverse
from .forms import StorageForm
from django.http import HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404

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


class UserStorageList(ListView):
    model = UserStorage
    #success_url = reverse_lazy('drinks:user_storage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StorageForm()
        return context

    
class StorageFormView(SingleObjectMixin, FormView):
    template_name = 'drinks/userstorage_list.html'
    form_class = StorageForm
    model = UserStorage

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        # self.object = self.get_object()

        new_item = UserStorage(user_ingredients = Ingredients.objects.get(id= request.POST.get('user_ingredients')),
                                user_id = self.request.user)
        new_item.save()
        # return self.get(self, request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('drinks:user_storage')


class UserStorageView(View):

    def get(self, request, *args, **kwargs):
        view = UserStorageList.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = StorageFormView.as_view()
        return view(request, *args, **kwargs)

    # def get_object(self):
    #     return get_object_or_404(User, pk=request.session['user_id'])

