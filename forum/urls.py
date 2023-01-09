from django.urls import path
from . import views
from .views import UpdateView

app_name = 'forum'

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('posts/', views.post_list, name='post_list'),
    path('create-post', views.create_post, name='create-post'),
]
