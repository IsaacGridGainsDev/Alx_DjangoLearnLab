from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from .models import Book, Library, Author
# Create your views here.

def book_list(request):
    books = Book.objects.all()
    context = {'book_list': books}
    return render(request, 'books/list_book.html', context)


class Library(DetailView):
    model = Library
    template_name = "library_detail.html"

    def get_context_data(Self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        

