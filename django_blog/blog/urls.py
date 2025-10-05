# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # other blog URLs (home, posts...) should be here too
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),

    # Login / logout using Django's built-in auth views but custom templates
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
]
