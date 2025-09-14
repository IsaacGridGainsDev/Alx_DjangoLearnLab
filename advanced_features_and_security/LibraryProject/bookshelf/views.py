from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .forms import ExampleForm
# Create your views here.

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.book_list', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})