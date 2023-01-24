from django.urls import path
from . import views
from .views import UpdatePostView, CreateCommentView, UpdateCommentView, DeletePostView, DeleteCommentView

app_name = 'forum'

urlpatterns = [
    path('sign-up', views.sign_up, name='sign-up'),
    path('posts/', views.post_list, name='post_list'), #todo number of pages
    path('create-post', views.create_post, name='create-post'),
    path('update-post/<int:pk>', UpdatePostView.as_view(), name='update-post'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name = 'delete-post'),
    path('create-comment/<int:pk>', CreateCommentView.as_view(), name='create-comment'),
    path('update-comment/<int:pk>', UpdateCommentView.as_view(), name='update-comment'),
    path('delete-comment/<int:pk>', DeleteCommentView.as_view(), name='delete-comment'),
    path('post/<int:pk>', views.post_detail, name='post-detail'),
    path('profile', views.profile, name='profile'),
]
