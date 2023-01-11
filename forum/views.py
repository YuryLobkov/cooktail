from django.shortcuts import render, redirect
from .forms import RegistrationForm, PostForm
from django.contrib.auth import login, logout, authenticate
from .models import Post, Comment
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView


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

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'forum/update_post.html'
    fields = ['title', 'content']
    success_url = '/forum/posts'

class CreateCommentView(CreateView):
    model = Comment
    template_name = 'forum/create_comment.html'
    fields = ['post','body']
    success_url = '/forum/posts'

    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        return super().form_valid(form)

class UpdateCommentView(UpdateView):
    model = Comment
    template_name = 'forum/update_comment.html'
    fields = ['body']
    success_url = '/forum/posts'

class PostDetailView(DetailView):
    model = Comment
    fields = ['__all__']
    template_name = 'forum/post_detail.html'

