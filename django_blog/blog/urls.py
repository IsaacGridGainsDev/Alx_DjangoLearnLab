from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    # Post URLs below (Task 2)
]
