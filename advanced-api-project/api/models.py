from django.db import models
from datetime import date

# Create your models here.

class Author(models.Model):
    """
    Author here represents writers, and they can have multiple books
    THe name field stores the full name of the author
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book represents books written by authors
    and has a title fireld for the ook title, publication year, that year the book was released
    and an author field that references the Author model, otherwise called a foreign key
    """

    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    