from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
import json
import base64
from .models import *
from Crypto.Cipher import AES

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
    if request.method == "POST":
        data = request.body
        data = json.loads(data[0:len(data)])
        temp = len('data:image/png;base64,')
        user_image_b64 = data["user-image"]
        password = data["password"]
        
        user_image_bytes_str = user_image_b64[temp:len(user_image_b64)]
        img_data = base64.b64decode(user_image_bytes_str)
        private_key = str.encode((password + password)[0:16])
        iv = str.encode((password + password)[0:16])
        cfb_cipher = AES.new(private_key, AES.MODE_CFB, iv)
        
        encrypted_img = cfb_cipher.encrypt(img_data)

        cfb_decipher = AES.new(private_key, AES.MODE_CFB, iv)
        plain_data = cfb_decipher.decrypt(encrypted_img)
        output_file = open("output.jpg", "wb")
        output_file.write(plain_data)
        output_file.close()
        """
        with open('rrr.png', 'wb') as f:
            f.write(imgdata)
        """
    return render(request, 'index.html')
    return;
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
    