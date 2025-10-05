# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm
from taggit.models import Tag


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
    def get_queryset(self):
            """
            Supports:
            - q=search_term  -> searches title, content, and tag names
            - ordering via ?ordering=published_date or ?ordering=-published_date
            Also uses select_related/prefetch_related to optimize DB queries.
            """
            qs = Post.objects.select_related("author").prefetch_related("tags").all()

            q = self.request.GET.get("q", "").strip()
            if q:
                # Search across title, content and tag name using Q objects
                qs = qs.filter(
                    Q(title__icontains=q) |
                    Q(content__icontains=q) |
                    Q(tags__name__icontains=q)
                ).distinct()

            # Optional ordering param
            ordering = self.request.GET.get("ordering")
            if ordering:
                qs = qs.order_by(ordering)

            return qs


class PostsByTagView(ListView):
    """
    List posts for a tag (URL: /tags/<str:tag>/)
    """
    model = Post
    context_object_name = "posts"
    template_name = "blog/posts/post_list.html"
    paginate_by = 10

    def get_queryset(self):
        tag = self.kwargs.get("tag")
        # prefetch tags and author to reduce queries
        if TagWidget:
            qs = Post.objects.select_related("author").prefetch_related("tags").filter(tags__name__iexact=tag)
        else:
            qs = Post.objects.filter(tags__name__iexact=tag)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag"] = self.kwargs.get("tag")
        return ctx

# View single post - public
class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/posts/post_detail.html"
    def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            # include comment form and the post's comments
            ctx.setdefault("comment_form", CommentForm())
            ctx["comments"] = self.object.comments.select_related("author").all()
            return ctx

    def post(self, request, *args, **kwargs):
        # Handle new comment submission on the post detail page
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect(f"{reverse_lazy('login')}?next={request.path}")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            return redirect(self.object.get_absolute_url())
        # On error, re-render detail with form errors
        context = self.get_context_data()
        context["comment_form"] = form
        return self.render_to_response(context)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comments/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comments/comment_form.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comments/comment_confirm_delete.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user
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