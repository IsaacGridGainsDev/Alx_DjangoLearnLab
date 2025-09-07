from django.urls import Path
from . import views

urlpatterns = [
        path('books/', views.book_list, name='books'),
        path('library/', views.Library.as_view(), name='Library'),
        ]
