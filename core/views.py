from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests


@csrf_exempt
def sign_in(request):
    return render(request, 'main/sign-in.html')


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the  user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)
    
    user, created = User.objects.get_or_create(email = user_data['email'])
    if created:
        user.username = user_data['email']
        user.set_unusable_password()
        user.save()
    
    # In a real app, I'd also save any new user here to the database.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data
    login(request, user)
    print(user_data)

    return redirect('sign_in')


def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')

