from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend

class BookListView(generics.ListAPIView):
    """
    A ListAPIView is used to list all the books. The queryset is set to all the
    books in the database. The serializer_class is set to BookSerializer which
    defines the data structure of the books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # The filter_backends attribute is set to a list containing the DjangoFilterBackend class. This allows users to filter books based on specific attributes.
    filter_backends = [DjangoFilterBackend]
    # The filterset_fields attribute is set to a list containing the fields that users can filter books by.
    filterset_fields = ['title','author__name', 'publication_year']
    # The search_fields attribute is set to a list containing the fields that users can search books by.
    search_fields = ['title', 'author__name', 'publication_year']
    # The ordering_fields attribute is set to a list containing the fields that users can order books by.
    ordering_fields = ['title', 'author__name', 'publication_year']

class BookDetailView(generics.RetrieveAPIView):
    """
    A RetrieveAPIView is used to retrieve a specific book. The queryset is set to
    all the books in the database. The serializer_class is set to BookSerializer
    which defines the data structure of the books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BookCreateView(generics.CreateAPIView):
    """
    A CreateAPIView is used to create a new book. The serializer_class is set to
    BookSerializer which defines the data structure of the books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print("A new book is being created")
# Create your views here.


    def perform_create(self, serializer):
        print("A new book is being created")
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    An UpdateView is used to update a specific book. The serializer_class is set to
    BookSerializer which defines the data structure of the books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        print("A book is being updated")
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    A DestroyAPIView is used to delete a specific book. The serializer_class is set to
    BookSerializer which defines the data structure of the books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', "publication_year"]