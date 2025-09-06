from bookshelf.models import Book

book1 = Book(title="1984", author="George Orwell", publ
   ...: ication_year=1949)

In [3]: book1.save()

In [9]: Book.objects.all()
# Out[9]: <QuerySet [<Book: 1984 by George Orwell>]>
~                                                               ~                                                   

In [19]: print(book1.id, book1.title, book1.author, book1.publi
    ...: cation_year)
# 1 1984 George Orwell 1949

In [10]: book2 = book1

In [11]: book2.title = "Nineteen Eighty-Four"

In [12]: book2.save()

In [13]: Book.objects.all()
# Out[13]: <QuerySet [<Book: Nineteen Eighty-Four by George Orwell>]>
~                                                               ~


In [20]: book2.delete()
# Out[20]: (1, {'bookshelf.Book': 1})                           ~                                                               ~                                                               ~                                                               ~                                                               ~                                                               ~                                                               ~                                                               ~                                                               ~                                                               ~                                                               ~                                                               ~                                                               ~                                          
