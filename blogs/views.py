from django.db.models import Count
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related('user').prefetch_related(
        'post_comments',
        'post_likes',
        'post_audios',
        'post_images',
        'post_videos'
    ).annotate(
        likes_count=Count('post_likes', distinct=True),
        comments_count=Count('post_comments', distinct=True)
    )
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
