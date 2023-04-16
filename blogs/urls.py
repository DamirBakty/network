from . import views
from django.urls import path, include

app_name = 'blog'

urlpatterns = [
    path('post/', views.PostListCreateAPIView.as_view()),
    path('post/<int:pk>', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path('post_like/<int:pk>', views.PostLikeAPIView.as_view()),
    path('comment/<int:pk>', views.CommentListCreateAPIView.as_view())
]
