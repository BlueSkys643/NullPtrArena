from django.urls import path
from . import views

urlpatterns = [
    path("submit/", views.submit, name="submit"),
    path("home/", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]