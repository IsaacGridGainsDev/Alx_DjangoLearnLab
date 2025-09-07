from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, AdminView, LibrarianView, MemberView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', views.list_books, name='books'),
    path('library/', views.LibraryDetailView.as_view(), name='Library'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path("admin-dashboard/", AdminView.as_view(), name="admin_page"),
    path("librarian-dashboard/", LibrarianView.as_view(), name="librarian_page"),
    path("member-dashboard/", MemberView.as_view(), name="member_page"),
]
