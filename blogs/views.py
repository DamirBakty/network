from django.db.models import Count, OuterRef, Subquery, Exists
from rest_framework import generics
from .models import Post, Comment, PostLike, PostAudio, PostImage, PostVideo
from blogs import serializers
from django.db import transaction

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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.PostCreateSerializer
        return serializers.PostListSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(user=self.request.user)
            image_serializer = serializers.ImageCreateSerializer(data=self.request.data)
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save(post=serializer.instance, user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


        

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostListSerializer
    lookup_field = 'pk'
