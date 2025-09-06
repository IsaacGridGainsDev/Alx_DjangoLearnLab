author = Book.author.filter(name="George Orwell")
a1 = Author.objects.get(name=author_name)
#objects.filter(author=author)
a1.objects.filter(author=author)

books = Library.books.all()
b1 = Library.objects.get(name=library_name)
librarian = Librarian.library.get(name="LBS")

