from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Post, Comment
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from ckeditor.widgets import CKEditorWidget


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Required. Enter a valid email adress.', required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

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
        exclude = ('date_joined',)
    
        fields = ['first_name',
                  'last_name',
                  'email',
                  'image',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            style_data = {
                'class': 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(style_data)
        self.fields['first_name'].widget.attrs.update({'placeholder' : 'First name',})
        self.fields['last_name'].widget.attrs.update({'placeholder' : 'Last name'})
        self.fields['email'].widget.attrs.update({'placeholder' : 'Email',
                                                  'style': 'none'})
        

class PasswordChangeForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())    


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})

class CommentForm(forms.ModelForm):
    body = CKEditorWidget(config_name='comment_section')

    class Meta:
        model = Comment
        fields = ['body']
        