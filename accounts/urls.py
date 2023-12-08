from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    # auth
    path("signup/", views.signup_user, name="signup_user"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
]
