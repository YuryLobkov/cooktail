from django.urls import path
from . import views
from .views import UpdatePostView

app_name = 'forum'

urlpatterns = [
    path('', views.home, name='home'),
    # path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('posts/', views.post_list, name='post_list'),
    path('create-post', views.create_post, name='create-post'),
    path('update-post/<int:pk>', UpdatePostView.as_view(), name='update-post'),
]
