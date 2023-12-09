from django.urls import path
from . import views

# Create different uri roots to connect them to a view 
urlpatterns = [
    path("login/", views.login, name="login"),
    path("auth/", views.auth, name="auth"),
    path("auth_callback/", views.auth_callback, name="auth_callback"),
    path("", views.home, name="home"),
]

