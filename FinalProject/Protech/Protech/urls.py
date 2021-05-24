"""Protech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from home import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls), # GET
    path('', views.home, name='home'), # GET
    path('register_page', views.register_get, name='register_page'), # GET
    path('/register/', views.register_post, name='register'), # POST
    path('login_page', views.login_get , name='login_page'), # GET
    path('login/', views.login_post , name='login'), # POST
    path('error_page', views.error_get , name='error_page'), # GET
    path('profile_page', login_required(views.profile_get), name='profile_page'), # GET
]
