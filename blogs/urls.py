from . import views
from django.urls import path, include

app_name = 'blog'

urlpatterns = [
    path('post/', views.PostListCreateAPIView.as_view()),
    path('post/<int:pk>', views.PostRetrieveUpdateDestroyAPIView.as_view()),
]
