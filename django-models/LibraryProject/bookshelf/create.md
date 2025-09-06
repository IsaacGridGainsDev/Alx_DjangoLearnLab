 book1 = Book(title="1984", author="George Orwell", publ
   ...: ication_year=1949)

Book.objects.create(title="1984, author="George Orwell", publ
   ...: ication_year=1949)

In [3]: book1.save()

In [9]: Book.objects.all()
# Out[9]: <QuerySet [<Book: 1984 by George Orwell>]> 
