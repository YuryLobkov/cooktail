from django.shortcuts import render, redirect
from .forms import RegistrationForm, PostForm
from django.contrib.auth import login, logout, authenticate
from .models import Post, Comment
from django.views.generic import UpdateView, CreateView


# Create your views here.
def home(request):
    return render(request, 'forum/home.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/sign_up.html', context={'form':form})

def post_list(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()    
    return render(request, 'forum/post_list.html', {'posts':posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/forum/posts')
    else:
        form = PostForm()
    return render(request, 'forum/create_post.html', {'form':form})

class CreateCommentView(CreateView):
    model = Comment
    template_name = 'forum/create_comment.html'
    fields = ['post','name', 'body']
    success_url = '/forum/posts'

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'forum/update_post.html'
    fields = ['title', 'content']
    success_url = '/forum/posts'
    

# def update_post(request):
#     posts = Post.objects.all()
#     if request.method == 'POST':
#         post_id = request.POST.get('post-id')
#         post = Post.objects.filter(id=post_id).first()
#         if post and post.author == request.user:
#             post.update()
#     return render(request, 'forum/post_list.html', {'posts':posts})