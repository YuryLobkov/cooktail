"""cooktail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import start_redirect_view
from django.conf.urls.static import static
from django.conf import settings
from forum.views import sign_up, custom_login, custom_logout, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drinks/', include('drinks.urls'), name='drinks'),
    path('', start_redirect_view, name='start_page'),
    path('forum/', include('forum.urls'), name='forum'),
    path('sign_up/', sign_up, name='sign-up'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/<username>', profile, name='profile'),
    # path('profile/<username>', views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
