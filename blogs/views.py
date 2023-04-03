from django.db.models import Count, OuterRef, Subquery, Exists
from rest_framework import generics
from .models import Post, Comment, PostLike, PostAudio, PostImage, PostVideo
from .serializers import PostSerializer
from django.db import connection
from django.db.models import Prefetch
from django.db import models


class PostListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Post.objects.select_related('user').prefetch_related(
    #     'post_comments',
    #     'post_likes',
    #     'post_audios',
    #     'post_images',
    #     'post_videos'
    # ).annotate(
    #     likes_count=Count('post_likes', distinct=True),
    #     comments_count=Count('post_comments', distinct=True)
    # )
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        conn = connection
        likes_subquery = PostLike.objects.filter(post=OuterRef('pk')).values('post').annotate(count=Count('id')).values('count')
        comments_subquery = Comment.objects.filter(post=OuterRef('pk')).values('post').annotate(count=Count('id')).values('count')

        posts = Post.objects.annotate(
            likes_count=Subquery(likes_subquery, output_field=models.IntegerField()),
            comments_count=Subquery(comments_subquery, output_field=models.IntegerField()),
        ).select_related('user')
        
        print(len(posts))
        
        print(len(conn.queries))
        # print(conn.queries)
        for i in conn.queries:
            print(i)
            print('----------')
        return posts
        

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
