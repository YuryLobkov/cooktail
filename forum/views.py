from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import RegistrationForm, PostForm, CommentForm, UserEditForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from .models import Post, Comment
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('start_page')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Your account {user.username} has been created!')
            return redirect('start_page')
        
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', context={'form':form})

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('start_page')
    
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'You have been successfully logged in as {user.username}!')
                return redirect('start_page')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form =  AuthenticationForm()

    return render(request, 'registration/login.html', {'form':form})

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('start_page')




def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    comments = Comment.objects.all()
    paginagor = Paginator(posts, 1)
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

class UpdatePostView(UpdateView, LoginRequiredMixin): #done
    model = Post
    template_name = 'forum/update_post.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DeletePostView(DeleteView, LoginRequiredMixin): #done
    model = Post
    success_url = '/forum/posts'
       
class CreateCommentView(CreateView, LoginRequiredMixin): #done
    
    model = Comment
    template_name = 'forum/create_comment.html'
    fields = ['body']

    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        return super().form_valid(form)

class UpdateCommentView(UpdateView, LoginRequiredMixin): #done
    model = Comment
    template_name = 'forum/update_comment.html'
    fields = ['body']
    
    #HOW TO OVERWRITE DEFAULT GET SUCCESS URL
    def get_success_url(self, **kwargs):
        post_id = self.object.post.id #HOW TO GET POST ID FOR FUTHER USE TO REDIRECT BY PK                           
        return reverse('forum:post-detail', kwargs={'pk': post_id})

class DeleteCommentView(DeleteView, LoginRequiredMixin): #done
    model = Comment

    #HOW TO OVERWRITE DEFAULT GET SUCCESS URL
    def get_success_url(self, **kwargs):
        post_id = self.object.post.id #HOW TO GET POST ID FOR FUTHER USE TO REDIRECT BY PK                           
        return reverse('forum:post-detail', kwargs={'pk': post_id})
    
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

# def profile(request, username):
#     if request.method == "POST":
#         user = request.user
#         form = UserEditForm(request.POST, request.FILES, instance = user)
#         if form.is_valid():
#             user_form = form.save()
#             messages.success(request, f'{user_form.username}, your profile has been updated!')
#             return redirect('forum:profile', user_form.username)
        
#         for error in list(form.errors.values()):
#             messages.error(request, error)

#     user = User.objects.filter(username=username).first()
#     if user:
#         form = UserEditForm(instance=user)
#         return render(request,'registration/profile.html', {'form':form} )
    
#     return redirect('home')