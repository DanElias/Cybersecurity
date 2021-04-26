from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

"""
    TO-DO:
    1) 404 Page
    2) Cuando haya error en el register (username duplicado) te diga que ya existe
    3) Cuando haya error en el register (email duplicado) te diga que ya existe
    4) Que te diga que la contraseña debe de cumplir y validarlo en el back
    - Your password can’t be too similar to your other personal information.
    - Your password must contain at least 8 characters.
    - Your password can’t be a commonly used password.
    - Your password can’t be entirely numeric.
    5) Checar a donde nos redireccionan los errores
"""

def home(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render({},request))

# GET
def register_get(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render({},request))

# POST
def register_post(request):
    try:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.create_user(username, email, password)
        user.save()
        return HttpResponseRedirect('/login_page')
    except:
        return HttpResponseRedirect('/error_page')

# GET
def login_get(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render({},request))

# POST
def login_post(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/profile_page')
        else:
            return HttpResponseRedirect('/login_page')
    except:
        return HttpResponseRedirect('/error_page')

# GET
def error_get(request):
    template = loader.get_template('error.html')
    return HttpResponse(template.render({},request))

# GET
def profile_get(request):
    template = loader.get_template('profile.html')
    return HttpResponse(template.render({},request))
    