from django.urls import path

from api_project.api_project.urls import urlpatterns
from .views import BookList

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
]