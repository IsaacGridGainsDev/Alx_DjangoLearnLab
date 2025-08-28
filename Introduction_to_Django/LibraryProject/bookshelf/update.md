In [10]: book2 = book1

In [11]: book2.title = "Nineteen Eighty-Four"

In [12]: book2.save()

In [13]: Book.objects.all()
# Out[13]: <QuerySet [<Book: Nineteen Eighty-Four by George Orwell>]>
