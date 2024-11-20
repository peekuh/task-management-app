from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views import View
import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.utils.decorators import method_decorator

class GoogleLogin(View):

    
    def get(self, request, event):
        if event == "login":    
            return self.sign_in(request)
        elif event == "callback":
            return self.auth_receiver(request)
        elif event == "logout":
            return self.sign_out(request)
        

    @method_decorator(csrf_exempt)
    def post(self, request, event):
        if event == "callback":
            return self.auth_receiver(request)
        return HttpResponse(status=404)
    
    def sign_in(self, request):
        return render(request, 'main/sign-in.html')

    
    @method_decorator(csrf_exempt)
    def auth_receiver(self, request):
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
        
        # In a real app, I'd also save any new user here to the database.
        # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
        user, created = User.objects.get_or_create(email = user_data['email'])
        if created:
            user.username = user_data['email']
            user.set_unusable_password()
            user.save()
        request.session['user_data'] = user_data
        login(request, user)
        print(user_data)

        return redirect('sign_in')


    def sign_out(self, request):
        del request.session['user_data']
        return redirect('sign_in', event = "login")