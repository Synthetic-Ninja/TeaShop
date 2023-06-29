from django.urls import path

from .views import login_registration
app_name = 'users'

urlpatterns = [path('login-registration/', login_registration, name='login_registration')]
