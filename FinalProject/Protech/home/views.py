from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
import json
import base64
from .models import *
from Crypto.Cipher import AES
from . import facelogin
import django.contrib.auth.password_validation as validators

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
        # Get data from the request's body as json
        data = request.body
        data = json.loads(data[0:len(data)])
        # obtain data fields
        username = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirm_password"]
        user_image_b64 = data["user_image"]
        # this is a string that comes at the beginning of the base64 image string
        temp = len('data:image/png;base64,')
        # we get only the base64 bytes without the temp string
        user_image_bytes_str = user_image_b64[temp:len(user_image_b64)]
        # decode the base64 string
        img_data = base64.b64decode(user_image_bytes_str)
        # set a private key that originates from the user's password (16 bytes)
        private_key = str.encode((password + password)[0:16])
        iv = str.encode((password + password)[0:16])
        # Create AES encryptor object
        cfb_cipher = AES.new(private_key, AES.MODE_CFB, iv)
        # Encrypt the image
        encrypted_img = cfb_cipher.encrypt(img_data)
        # Save the user
        user = User.objects.create_user(username, email, password)
        user.profile.biometric_data = encrypted_img
        user.save()
        return JsonResponse({'code': 200})
    except Exception as e:
        print(e)        
        return JsonResponse({'code': 500})

# GET
def login_get(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render({},request))

# POST
def login_post(request):
    try:
        # Get data from the request's body as json
        data = request.body
        data = json.loads(data[0:len(data)])
        # obtain data fields
        username = data["username"]
        password = data["password"]
        user_image_b64 = data["user_image"]
        # this is a string that comes at the beginning of the base64 image string
        temp = len('data:image/png;base64,')
        # we get only the base64 bytes without the temp string
        user_image_bytes_str = user_image_b64[temp:len(user_image_b64)]
        # decode the base64 string
        captured_user_img = base64.b64decode(user_image_bytes_str)
        # set a private key that originates from the user's password (16 bytes)
        private_key = str.encode((password + password)[0:16])
        iv = str.encode((password + password)[0:16])
        
        #Get user's biometric data (photo)
        user = User.objects.get(username=username)
        encrypted_img = user.profile.biometric_data
        
        # Create AES decryptor object
        cfb_decipher = AES.new(private_key, AES.MODE_CFB, iv)
        # Decrypt the image
        user_image_db = cfb_decipher.decrypt(encrypted_img)

        # Face recognition authentication
        face_auth = facelogin.FaceAuth()
        isFaceAuthenticated = face_auth.authenticate(user_image_db, captured_user_img)
        if not isFaceAuthenticated:
            return JsonResponse({'code': 401})
        # Authenticate
        user = authenticate(request, username=username, password=password)
        return JsonResponse({'code': 201})
    except Exception as e:
        return JsonResponse({'code': 500})

# GET
def error_get(request):
    template = loader.get_template('error.html')
    return HttpResponse(template.render({},request))

    # GET
def unauthorized_get(request):
    template = loader.get_template('unauthorized.html')
    return HttpResponse(template.render({},request))

# GET
def profile_get(request):
    template = loader.get_template('profile.html')
    return HttpResponse(template.render({},request))
    