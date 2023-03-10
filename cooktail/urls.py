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
from django.conf.urls import handler404
from forum.views import sign_up, custom_login, custom_logout, profile, \
                        activate, password_change, password_reset, \
                        password_reset_confirm
import os


urlpatterns = [
    path(str(os.getenv('ADMIN_URL')), admin.site.urls),
    path('drinks/', include('drinks.urls'), name='drinks'),
    path('', start_redirect_view, name='start_page'),
    path('forum/', include('forum.urls'), name='forum'),
    path('sign_up/', sign_up, name='sign-up'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/<username>', profile, name='profile'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('password_change', password_change, name='password_change'),
    path('password_reset', password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>', password_reset_confirm, name='password_reset_confirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "forum.views.error_404"    