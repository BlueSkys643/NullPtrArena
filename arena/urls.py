from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("submit/", views.submit, name="submit"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path(
        "problem-set/<int:id>/",
        views.problem_set,
        name="problem_set",
    ),
]