# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Post

class CustomUserCreationForm(UserCreationForm):
    """
    Registration form that includes email.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user

from .models import Post
try:
    from taggit.forms import TagWidget
    TAG_WIDGET = TagWidget
except Exception:
    TagWidget = None
    TAG_WIDGET = forms.TextInput
class PostForm(forms.ModelForm):
    """
    ModelForm for Post creation and editing.
    Fields: title, content. Author is set automatically in the view.
    """
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter post title", "class": "form-control"}),
            "content": forms.Textarea(attrs={"placeholder": "Write your post...", "class": "form-control", "rows": 10}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

class CommentForm(forms.ModelForm):
    """
    Simple form for creating/updating comments.
    """
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment..."}), max_length=2000)

    class Meta:
        model = Comment
        fields = ["content"]

    def clean_content(self):
        data = self.cleaned_data.get("content", "").strip()
        if not data:
            raise forms.ValidationError("Comment cannot be empty.")
        return data
 #views.py — CRUD views using generics + mixins
#Add to blog/views.py (or update):

# blog/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

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