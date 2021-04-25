from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


def home(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render({},request))

def register(request):
    print(request.POST)
    fullname = request.POST['fullname']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    user = User.objects.create_user(fullname, email, password)
    user.save()
    return HttpResponseRedirect('register.html')