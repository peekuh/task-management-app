from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
import os
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from django.utils.crypto import get_random_string
from .models import Tasks
import json

@method_decorator(csrf_exempt, name= 'dispatch')
class GoogleLogin(View):
    def get(self, request, event):
        if event == "login":    
            return self.sign_in(request)
        elif event == "logout":
            return self.sign_out(request)       
           
    def post(self, request, event):    
        if event == "callback":
            return self.auth_receiver(request)
        return HttpResponse(status=404)
    
    def sign_in(self, request):
        return render(request, 'main/sign-in.html')

    def auth_receiver(self, request):
        """
        Google calls this URL after the  user has signed in with their Google account.
        """
        print('Inside')
        token = request.POST.get('credential')
        try:
            user_data = id_token.verify_oauth2_token(
                token, requests.Request(), getattr(settings, "GOOGLE_OAUTH_CLIENT_ID")
            )
        except ValueError:
            return HttpResponse(status=403)
        
        # In a real app, I'd also save any new user here to the database.
        # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
        user, created = User.objects.get_or_create(
            email = user_data['email'],
            defaults = {"username" : f'user_{get_random_string(8)}'}
        )
        
        if created:
            user.set_unusable_password()
            user.save()
        request.session['user_data'] = user_data
        login(request, user)
        print("print userdata", user_data)
        url =  url = reverse('sign_in', kwargs={'event': 'login'})
        return HttpResponseRedirect(url)

    def sign_out(self, request):
        del request.session['user_data']
        return redirect('sign_in', event = "login")

@method_decorator(csrf_exempt, name= 'dispatch')
class TaskManagement(View):
    def get(self, request):
        return render(request, 'main/tasks.html')
    
    def post(self, request):
        if request.POST["event"] == "task.create":
            title = request.POST['title']
            description = request.POST['description']
            Tasks.objects.create(
                user = request.user,
                title = title,
                description = description
            )
            return HttpResponse("task created")
        
        elif request.POST["event"] == "task.edit":
            Tasks.objects.filter(id = request.POST["chat_id"]).update(title = request.POST["task_title"])
            return HttpResponse("task updated")

        elif request.POST["event"] == "task.delete":
            Tasks.objects.get(id = request.POST["chat_id"]).delete()
            return HttpResponse("task deleted")


        

