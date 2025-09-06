author = Book.author.filter(name="George Orwell")
a1 = Author.objects.filter(name=author_name)

books = Library.books.all()
b1 = Library.objects.get(name=library_name)
librarian = Librarian.library.get(name="LBS")

