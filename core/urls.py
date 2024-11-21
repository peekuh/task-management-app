from django.urls import path
from . import views

urlpatterns = [
    path('auth/<str:event>', views.GoogleLogin.as_view(), name='sign_in'),
]