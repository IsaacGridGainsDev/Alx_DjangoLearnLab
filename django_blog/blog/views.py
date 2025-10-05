# blog/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

class UserLoginView(auth_views.LoginView):
    template_name = "blog/login.html"

class UserLogoutView(auth_views.LogoutView):
    template_name = "blog/logout.html"

class RegisterView(View):
    """
    GET: show registration form
    POST: validate and create user, redirect to login
    """
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "blog/register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect("login")
        return render(request, "blog/register.html", {"form": form})

@login_required
def profile_view(request):
    # placeholder simple profile view (extend as needed)
    return render(request, "blog/profile.html", {})
