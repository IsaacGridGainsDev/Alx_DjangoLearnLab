from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
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
    #'relationship_app.library_detail.html'
    template_name = "relationship_app/library_detail.html"

    def get_context_data(Self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        

