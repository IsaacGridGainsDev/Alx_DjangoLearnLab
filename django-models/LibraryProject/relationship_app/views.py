from django.shortcuts import render, redirect
from djang.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from .models import UserProfile
# Create your views here.

def list_books(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    model = Library
    fields = {'title', 'author', 'description'}
    #'relationship_app.library_detail.html'
    template_name = "relationship_app/library_detail.html"
    success_url = reverse_lazy('list_books')

    def get_context_data(Self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        
class RegisterView(CreateView):
    #creating the base class wiht UserCreationForm()
    form_class = UserCreationForm
    suucess_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'


#--------------------this section is redundant and was heavily relied upon from generative sources--------------
"""from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

 helper decorator
def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")
            if request.user.userprofile.role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to view this page.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@login_required
@role_required(allowed_roles=["Admin"])
def admin_view(request):
    return render(request, "admin_page.html", {"user": request.user})

@login_required
@role_required(allowed_roles=["Librarian"])
def librarian_view(request):
    return render(request, "librarian_page.html", {"user": request.user})

@login_required
@role_required(allowed_roles=["Member"])
def member_view(request):
    return render(request, "member_page.html", {"user": request.user})"""
#-------------------------------------------------####

"""
@login_required
def admin_view(request):
    if request.user.userprofile.role == "Admin":
        return render(request, "admin_page.html", {"user": request.user})

@login_required
def librarian_view(request):
    if request.user.userprofile.role == "Librarian":
        return render(request, "librarian_page.html", {"user": request.user})
    return HttpResponseForbidden("Not Authorized")

@login_required
def member_view(request):
    if request.user.userprofile.role == "Member":
        return render(request, "member_page.html", {"user":request.user})
    return HttpResponseForbidden("Not Authorized")

def signup_view(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]

        user = user.objects.create_user(username=username, email=email, password=password)

        user.userprofile.role = role
        user.userprofile.save()

        logn(request, user)
        return redirect("library")
    return render(request, "register.html")

"""
# Helpers
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Admin View
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


# Librarian View
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')


# Member View
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html')
