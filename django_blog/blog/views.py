from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'blog/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

def home(request):
    return render(request, 'blog/home.html')

def posts(request):
    return render(request, 'blog/posts.html')