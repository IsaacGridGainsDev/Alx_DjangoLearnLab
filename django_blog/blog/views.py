from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib import messages
from .forms import CustomUserCreationForm

# built-in login/logout views
class UserLoginView(LoginView):
    template_name = 'blog/login.html'

class UserLogoutView(LogoutView):
    template_name = 'blog/logout.html'

# custom register view
class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "blog/register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created. You can now log in.")
            return redirect("login")
        return render(request, "blog/register.html", {"form": form})
