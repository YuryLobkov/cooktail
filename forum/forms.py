from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class RegistrationForm(UserCreationForm):
    model = User
    fields = ['__all__']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('title', css_class='form-control custom-form-field'),
        Field('content', css_class='form-control custom-form-field')
    )
    helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))