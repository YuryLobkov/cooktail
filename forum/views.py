from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
"""
IMPORT FROM PROJECT FILES
"""
from .forms import RegistrationForm, PostForm, CommentForm, UserUpdateForm, \
                   PasswordChangeForm, PasswordResetForm
from .models import Post, Comment
"""
AUTH AND EMAIL CONFIRMATION IMPORTS
"""
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from .tokens import activation_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.http import Http404
from .forms import UserLoginForm
from django.contrib import messages
from django.template import Context
from .decorators import user_is_not_authenticated
from .mixins import IsPostAuthorMixin, IsCommentAuthorMixin

# Create your views here.
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, f'You have passed email confirmation. Now you can log-in!')
        return redirect('login')
    else:
        messages.error(request, f'Confirmation link is invalid. Maybe it is already expired')
    return redirect('start_page')


def email_activate(request, user, to_email):
    subject = 'Cooktail - portal for bartenders! Account activation.'
    data_context = {
        'user': user.username,
        'domain':get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    }
    message = get_template('user/email_template_account_activation.html').render(data_context)
    email = EmailMessage(subject, message, to=[to_email])
    email.content_subtype = 'html'
    if email.send():
        messages.success(request, f'<b>{user}</b>, to complete the registration, \
                         you need to pass <b>email confirmation.</b> \n Please, go \
                         to your <b>{to_email}</b> inbox and check it. There should \
                         be an email with instructions that we sent you!')
    else:
        messages.error(request, f'We have some problem with sending email to {email}.\
                                  Did you type it correctly?')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('start_page')    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            email_activate(request, user, form.cleaned_data.get('email'))
            return redirect('start_page')        
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error [0] == 'This field is required.':
                    messages.error(request, 'You must pass reCAPTCHA')
                    continue                
                messages.error(request, error)
    else:
        form = RegistrationForm()
    return render(request, 'user/sign_up.html', context={'form':form})


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed!')
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = PasswordChangeForm(user)
    return render(request, 'user/password_change_confirmation.html', {'form':form})


@user_is_not_authenticated
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = 'Cooktail - portal for bartenders! Password reset.'
                data_context = {
                    'user': associated_user,
                    'domain':get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': activation_token.make_token(associated_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                }
                message = get_template('user/email_template_password_reset.html').render(data_context)
                email = EmailMessage(subject, message, to=[associated_user.email])
                email.content_subtype = 'html'
                if email.send():
                    messages.success(request, 
                        """
                        <b>Password reset sent</b><hr>
                        <p>We have send you an email with instructions. If an account with \
                        such an email exists,you will recieve it shortly!</p>
                        """
                    )
                else:
                    messages.error(request, 'We have problems with sending to \
                                             you a password reset email.')
            return redirect('start_page')               
        for key, error in list(form.errors.items()):
            if key == 'captcha' and error [0] == 'This field is required.':
                messages.error(request, 'You must pass reCAPTCHA')
                continue         
            messages.error(request, error)     
    form = PasswordResetForm()
    return render(request, 'user/password_reset_confirmation.html', {'form':form})


def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and activation_token.check_token(user, token):
        if request.method == "POST":
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your password has been set!')
                return redirect('start_page')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        form = PasswordChangeForm(user)    
        return render(request, 'user/password_reset_confirmation.html', {'form':form})
    else:
        messages.error(request, f'Confirmation link is invalid. Maybe it is already expired')
    messages.error(request, 'Something went wrong...')
    return redirect('start_page')


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('start_page')
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f'You have been successfully logged in as {user.username}!')
                return redirect('start_page')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error [0] == 'This field is required.':
                    messages.error(request, 'You must pass reCAPTCHA')
                    continue
                messages.error(request, error)
    form =  UserLoginForm()
    return render(request, 'user/login.html', {'form':form})


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('start_page')


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    comments = Comment.objects.all()
    paginagor = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginagor.get_page(page_number)
    return render(request, 'forum/post_list.html', {'posts':posts,
                                                    'comments':comments,
                                                    'page_obj': page_obj,})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f'Post "{post.title}" has been successfully created!')
            return redirect('/forum/posts')
    else:
        form = PostForm()
    return render(request, 'forum/create_post.html', {'form':form})


class UpdatePostView(LoginRequiredMixin, IsPostAuthorMixin, UpdateView):  # Done.
    model = Post
    form_class = PostForm
    template_name = 'forum/update_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, DeleteView):  # Done.
    model = Post
    success_url = '/forum/posts'


class UpdateCommentView(LoginRequiredMixin, IsCommentAuthorMixin, UpdateView):  # Done.
    model = Comment
    template_name = 'forum/update_comment.html'
    fields = ['body']
    
    def get_success_url(self, **kwargs):   # How to overwrite default get success url.
        post_id = self.object.post.id  # How to get post id for the further use to redirect by pk.                           
        return reverse('forum:post-detail', kwargs={'pk': post_id})
    


class DeleteCommentView(LoginRequiredMixin, DeleteView, SuccessMessageMixin):  # Done.
    model = Comment
    

    def get_success_url(self, **kwargs):  # How to overwrite default get success url.
        post_id = self.object.post.id  # How to get post id for the further use to redirect by pk.                         
        return reverse('forum:post-detail', kwargs={'pk': post_id})

    success_message = 'Deleted'


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    ied = pk
    comments = Comment.objects.filter(post=post).order_by('-pk')
    if request.method == 'POST':
        cf = CommentForm(request.POST or None)
        if cf.is_valid():
            body = request.POST.get('body')
            comment = Comment.objects.create(
                post = post,
                comment_author = request.user,
                body = body
            )
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        cf = CommentForm()
    context = {
        'title':'post detail',
        'comments': comments,
        'object': post,
        'ied': ied,
        'comment_form': cf
    }
    return render(request, 'forum/post_detail.html', context)


def profile(request, username):
    count_user = get_user_model().objects.filter(username=username).first()
    post_count = Post.objects.filter(author=count_user).count()
    comment_count = Comment.objects.filter(comment_author=count_user).count()
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, your profile has been updated!')
            return redirect('profile', user_form.username)        
        for error in list(form.errors.values()):
            messages.error(request, error)
    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        
        return render(request,'user/profile.html', {'form': form, 
                                                    'post_count': post_count,
                                                    'comment_count': comment_count})   
    return redirect('start_page')


def error_404(request, exception):
    return render(request, '404.html')