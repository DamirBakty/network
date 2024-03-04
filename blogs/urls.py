from django.urls import path
from blogs.views.comments import CommentLikeAPIView, CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView
from blogs.views.posts import PostLikeAPIView, PostRetrieveUpdateDestroyAPIView, PostListCreateAPIView, PostMarkAPIView

app_name = 'blog'

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view()),
    path('posts/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('post_like/<int:pk>', PostLikeAPIView.as_view()),
    path('post_mark/<int:pk>', PostMarkAPIView.as_view()),
    path('post_comments/<int:pk>', CommentListCreateAPIView.as_view()),
    path('comments/<int:pk>', CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('comment_like/<int:pk>', CommentLikeAPIView.as_view()),
]
