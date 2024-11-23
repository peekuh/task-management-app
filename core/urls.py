from django.urls import path
from . import views
from django. contrib import admin

urlpatterns = [
    path('auth/<str:event>', views.GoogleLogin.as_view(), name='sign_in'),
    path('task/', views.TaskManagement.as_view(), name = 'taskmgmt'),
    path('admin/', admin.site.urls)
]