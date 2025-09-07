from django.shortcuts import render, redirect
from djang.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
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
