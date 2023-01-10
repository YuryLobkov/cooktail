from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class RegistrationForm(UserCreationForm):
    model = User
    fields = ['__all__']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']