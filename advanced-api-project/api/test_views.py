from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Author, Book

class TestBookAPI(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Chimamanda Ngozi Adichie")
        self.book = Book.objects.create(title="Half of a Yellow Sun", publication_year=2022, author=self.author)
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        def test_list_books(self):
           url = reverse("book-list")
           response = self.client.get(url)
           self.assertEqual(response.status_code, status.HTTP_200_OK)
           self.assertGreater(len(response.data), 0)

        def test_detail_book(self):
            url = reverse("book-detail", args=[self.book.id])
            response = self.client.get(url)
            self.assertIn(response.status_code, status.HTTP_200_OK)

        def test_create_book(self):
            url = reverse("book-create")
            data = {
                "title": "The Kite Runner",
                "publication_year": 2003,
                "author": self.author.id
            }
            response = self.client.post(url, data, format="json")
            self.assertIn(response.status_code, status.HTTP_401_UNAUTHORIZED)

        def test_update_book(self):
            url = reverse("book-update", args=[self.book.id])
            data = {
                "title": "The Kite Runner",
                "publication_year": 2003,
                "author": self.author.id
            }
            response = self.client.put(url, data, format="json")
            self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])

        def test_delete_book(self):
            url = reverse("book-delete", args=[self.book.id])
            response = self.client.delete(url)
            self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])

        def test_authenticated_create(self):
            self.client.login(username="testuser", password="testpassword")
            url = reverse("book-create")
            data = {
                "title": "The Kite Runner",
                "publication_year": 2003,
                "author": self.author.id
            }
            response = self.client.post(url, data, format="json")
            self.assertIn(response.status_code, status.HTTP_201_CREATED)