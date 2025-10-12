from django.urls import path
from .views import NotificationListView, NotificationMarkReadView

urlpatterns = [
    path('notificaitons/', NotificationListView.as_view(), name='notifications'),
    path('<int:pk>/read/', NotificationMarkReadView.as_view(), name='notification-read'),
    path('like/<int:pk>/', LikePostView.as_view(), name='like-post'),
    path('unlike/<int:pk>/', UnlikePostView.as_view(), name='unlike-post'),
    path('comment/<int:pk>/', LikeCommentView.as_view(), name='like-comment'),
    path('unlike-comment/<int:pk>/', UnlikeCommentView.as_view(), name='unlike-comment'),
    ]
