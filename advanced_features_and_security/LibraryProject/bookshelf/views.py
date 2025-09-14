from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
# Create your views here.

@permission_required('bookshelf.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})