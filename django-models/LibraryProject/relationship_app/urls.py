from django.urls import path
from . import views
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
        path('books/', views.list_books, name='books'),
        path('library/', views.LibraryDetailView.as_view(), name='Library'),
        path('register/', views.RegisterView.as_view(), name='register'
        path('login/', LoginView.as_view(template_name='relationship_app/login.html'),
        patj('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'),
        ]
