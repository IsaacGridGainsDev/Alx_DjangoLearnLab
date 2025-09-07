from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import AccessMixin
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.detail import DetailView
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

class RoleRequiredMixin(AccessMixin):
    role_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.role_required is None or not hasattr(request.user, 'userprofile') or request.user.userprofile.role != self.role_required:
            return HttpResponseForbidden("You do not have permission to view this page.")
        return super().dispatch(request, *args, **kwargs)

class Admin(RoleRequiredMixin, TemplateView):
    role_required = 'Admin'
    template_name = 'relationship_app/admin_page.html'

class LibrarianView(RoleRequiredMixin, TemplateView):
    role_required = 'Librarian'
    template_name = 'relationship_app/librarian_page.html'

class MemberView(RoleRequiredMixin, TemplateView):
    role_required = 'Member'
    template_name = 'relationship_app/member_page.html'
