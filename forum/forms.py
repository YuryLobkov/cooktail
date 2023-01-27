from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Required. Enter a valid email adress.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name', 'username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control',
               'placeholder': 'Username or email'}),
        label="Username or Email")
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control',
               'placeholder':'Password'}))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name',
                  'last_name',
                  'email',
                  'image']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(Field('body',css_class='form-control mt-2 mb-3'))
