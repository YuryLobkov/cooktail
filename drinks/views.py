from django.shortcuts import render
from django.views import View
from django.views.generic import (TemplateView, ListView, 
                                CreateView, DeleteView,
                                DetailView, FormView)
from .models import Cocktail, Ingredients, Inventory, UserStorage, UserTools
from django.urls import reverse_lazy, reverse
from .forms import StorageForm, ToolsForm
from django.http import HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

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

    def get_queryset(self):
        queryset = UserStorage.objects.filter(user_id = self.request.user)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_inventory'] = StorageForm()
        used_items = UserStorage.objects.filter(user_id = self.request.user.id).values_list('user_ingredients_id')
        unused_items = Ingredients.objects.exclude(id__in = used_items)
        context['form_inventory'].fields['user_ingredients'].queryset = Ingredients.objects.filter(id__in = (unused_items))
        return context


class UserToolsList(ListView):
    model = UserTools
    template_name = 'drinks/usertools_list.html'

    def get_queryset(self):
        queryset = UserTools.objects.filter(user_id = self.request.user)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_tools'] = ToolsForm()
        used_tools = UserTools.objects.filter(user_id = self.request.user.id).values_list('user_inventory_id')
        unused_tools = Inventory.objects.exclude(id__in = used_tools)
        context['form_tools'].fields['user_inventory'].queryset = Inventory.objects.filter(id__in = (unused_tools))
        return context

    
class StorageFormView(SingleObjectMixin, FormView):
    template_name = 'drinks/userstorage_list.html'
    form_class = StorageForm
    model = UserStorage

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        new_item = UserStorage(user_ingredients = Ingredients.objects.get(id= request.POST.get('user_ingredients')),
                                user_id = self.request.user)
        new_item.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('drinks:user_storage')


class ToolsFormView(SingleObjectMixin, FormView):
    template_name = 'drinks/usertools_list.html'
    form_class = ToolsForm
    model = UserTools

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        new_tool = UserTools(user_inventory = Inventory.objects.get(id= request.POST.get('user_inventory')),
                                user_id = self.request.user.id)
        new_tool.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('drinks:user_tools')


class UserToolsView(View):

    def get(self, request, *args, **kwargs):
        view = UserToolsList.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ToolsFormView.as_view()
        return view(request, *args, **kwargs)


class UserStorageView(View):

    def get(self, request, *args, **kwargs):
        view = UserStorageList.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = StorageFormView.as_view()
        return view(request, *args, **kwargs)

# TODO make mixin for both ingredients and tools views
# TODO unite 2 views of users storage in one
# class UserStorageView(UserToolsView, UserIngredientsView):
#     pass


class UserStorageDelete(DeleteView):
    model = UserStorage
    success_url = reverse_lazy('drinks:user_storage')

class UserToolsDelete(DeleteView):
    model = UserTools
    success_url = reverse_lazy('drinks:user_tools')


class UserDrinksList(DrinksList):
    template_name = 'drinks/user_ing_cocktail_list.html'
    context_object_name = 'cocktail_list'
    def get_queryset(self):

        #V1 (not working correctly)
        # allowed_ings = UserStorage.objects.filter(user_id = self.request.user.id).values_list('user_ingredients')
        # print ('allowed ings         ',allowed_ings)
        # forbidden_cocktails = Cocktail.objects.exclude(main_ingredients__in = allowed_ings).values_list('id')
        # print ('forbiden cocktails   ',forbidden_cocktails)
        # queryset = Cocktail.objects.exclude(id__in = forbidden_cocktails)# .values_list('id')
        # print (queryset)
        # return queryset

        allowed_ings = UserStorage.objects.filter(user_id = self.request.user.id).values_list('user_ingredients')
        forbidden_ings = Ingredients.objects.exclude(id__in = allowed_ings).values_list('id')
        allowed_cocktails_by_main_ings = Cocktail.objects.exclude(main_ingredients__in = forbidden_ings)
        allowed_cocktails = allowed_cocktails_by_main_ings.exclude(optional_ingredients__in = forbidden_ings)
        allowed_cocktails_by_main_ings = allowed_cocktails_by_main_ings.exclude(id__in = allowed_cocktails)

        queryset = {
            'by_main' : allowed_cocktails_by_main_ings,
            'by_all' : allowed_cocktails
        }
        return queryset
