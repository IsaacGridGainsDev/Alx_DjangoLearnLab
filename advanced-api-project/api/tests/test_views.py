from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book

class BookAPITests(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Chimamanda Ngozi Adichie")
        self.book = Book.objects.create(title="Half of a Yellow Sun", publication_year=2022, author=self.author)

        def test_list_books(self):
           url = reverse("book-list")
           response = self.client.get(url)
           self.assertEqual(response.status_code, status.HTTP_200_OK)
           self.assertGreater(len(response.data), 0)

        def test_create_book(self):
            url = reverse("book-list")
            data = {
                "title": "The Kite Runner",
                "publication_year": 2003,
                "author": self.author.id
            }
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)