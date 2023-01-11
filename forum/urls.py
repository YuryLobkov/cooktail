from django.urls import path
from . import views
from .views import UpdatePostView, CreateCommentView, UpdateCommentView, PostDetailView

app_name = 'forum'

urlpatterns = [
    path('', views.home, name='home'),
    # path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('posts/', views.post_list, name='post_list'),
    path('create-post', views.create_post, name='create-post'),
    path('update-post/<int:pk>', UpdatePostView.as_view(), name='update-post'),
    path('create-comment/<int:pk>', CreateCommentView.as_view(), name='create-comment'),
    path('udpate-comment/<int:pk>', UpdateCommentView.as_view(), name='update-comment'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
]
