from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, DetailView
from .models import Book, Library, UserProfile

# Create your views here.

def list_books(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'

# Helpers
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Views
@login_required
@user_passes_test(is_admin)
def Admin_view(request):
    return render(request, 'relationship_app/admin_page.html')

@login_required
@user_passes_test(is_librarian)
def Librarian_view(request):
    return render(request, 'relationship_app/librarian_page.html')

@login_required
@user_passes_test(is_member)
def Member_view(request):
    return render(request, 'relationship_app/member_page.html')
