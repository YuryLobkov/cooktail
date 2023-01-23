from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import RegistrationForm, PostForm, CommentForm
from django.contrib.auth import login, logout, authenticate
from .models import Post, Comment
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


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
    return render(request, 'forum/post_list.html', {'posts':posts})

@login_required
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

def profile(request):
    return render(request, 'forum/user/profile.html')