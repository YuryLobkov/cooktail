from django import forms
from .models import UserStorage, Ingredients
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class StorageForm(forms.ModelForm):
    class Meta:
        model = UserStorage
        fields = ['user_ingredients']
    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(Field('body',css_class='form-control mt-2 mb-3'))

    def __init__(self,*args,**kwargs):
        super (StorageForm,self ).__init__(*args,**kwargs)
        self.fields['user_ingredients'].queryset = Ingredients.objects.filter(name = 'Vodka')
