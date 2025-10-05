# blog/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
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
#  "method"
@login_required
def profile_view(request):
    # placeholder simple profile view (extend as needed)
    return render(request, "blog/profile.html", {})

# List all posts - public
class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/posts/post_list.html"
    paginate_by = 10  # optional

# View single post - public
class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/posts/post_detail.html"

# Create a post - user must be authenticated
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/posts/post_form.html"
    # LoginRequiredMixin will redirect to login automatically

    def form_valid(self, form):
        # set the post author to the currently logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update a post - only author can edit
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/posts/post_form.html"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# Delete a post - only author can delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/posts/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user