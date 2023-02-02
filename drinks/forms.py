from django import forms
from .models import UserStorage, Ingredients, UserTools, Cocktail, Inventory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class CustomSelectMultiple(forms.CheckboxSelectMultiple):
    option_inherits_attrs = False

class CreateIng(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields= '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ing_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }

class CreateInventory(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'inv_type': forms.Select(attrs={'class': 'form-control'}),
        }

class CreateCocktail(forms.ModelForm):
    class Meta:
        model = Cocktail
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control'}),
            'main_ingredients': CustomSelectMultiple(attrs={'class': 'form-control'}),
            'optional_ingredients': CustomSelectMultiple(attrs={'class': 'form-control'}),
            'tools': CustomSelectMultiple(attrs={'class': 'form-control'}),
            'recepie': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-lg'}),
        }
    


class StorageForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(StorageForm, self).__init__(*args, **kwargs)
        self.fields['user_ingredients'].label = ""
    
    
    class Meta:
        model = UserStorage
        fields = ['user_ingredients']
        widgets = {'user_ingredients': forms.Select(attrs={'class': 'form-control'})}


class ToolsForm(forms.ModelForm):
    class Meta:
        model = UserTools
        fields = ['user_inventory']
    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(Field('body',css_class='form-control mt-2 mb-3'))
