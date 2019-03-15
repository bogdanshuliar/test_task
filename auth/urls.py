from django.urls import path, include
from rest_auth.views import (
    LoginView, LogoutView)
from rest_auth.registration.views import RegisterView

urlpatterns = [

    path("registration/", RegisterView.as_view(), name='rest_register'),

    path("login/", LoginView.as_view(), name='rest_login'),

    path("logout/", LogoutView.as_view(), name='rest_logout'),

]
