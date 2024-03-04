from typing import Protocol, OrderedDict
from django.db import transaction
from django.db.models import Count
from rest_framework.generics import get_object_or_404

from blogs.models.posts import PostLike, Post, Postmark, PostImage, PostAudio, PostVideo


class PostListCreateReposInterface(Protocol):
    @staticmethod
    def create_post(data: OrderedDict): ...

    @staticmethod
    def get_posts(): ...


class PostGetUpdateDeleteReposInterface(Protocol):
    @staticmethod
    def get_post(pk: int, user=None): ...

    @staticmethod
    def like_post(post_id: int, user): ...

    @staticmethod
    def mark_post(post_id: int, user): ...


class PostGetUpdateDeleteReposV1:
    @staticmethod
    def like_post(post_id, user):
        obj, liked = PostLike.objects.get_or_create(post_id=post_id, user=user)
        if not liked:
            obj.delete()
        likes_count = PostLike.objects.filter(post_id=post_id).count()
        return {'liked': liked, 'likes_count': likes_count}

    @staticmethod
    def get_post(pk: int, user=None):
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
        if user:
            queryset.filter(user=user)

        post = get_object_or_404(
            queryset,
            pk=pk
        )
        return post

    @staticmethod
    def mark_post(post_id: int, user):
        obj, marked = Postmark.objects.get_or_create(post_id=post_id, user=user)
        if not marked:
            obj.delete()
        return {'marked': marked}


class PostListCreateReposV1:
    @staticmethod
    def create_post(data: OrderedDict):
        with transaction.atomic():
            user = data.pop('user')
            post_data = data.pop('post')
            post = Post.objects.create(**post_data, user=user)
            if 'image' in data:
                images = [
                    PostImage(
                        user=user,
                        image=i['image'],
                        post=post
                    ) for i in data.pop('image')
                ]
                PostImage.objects.bulk_create(images)
            if 'audio' in data:
                audios = [
                    PostAudio(
                        user=user,
                        audio=i['audio'],
                        post=post
                    ) for i in data.pop('audio')
                ]
                PostAudio.objects.bulk_create(audios)
            if 'video' in data:
                videos = [
                    PostVideo(
                        user=user,
                        video=i['video'],
                        post=post
                    ) for i in data.pop('video')
                ]
                PostVideo.objects.bulk_create(videos)

    @staticmethod
    def get_posts():
        return Post.objects.select_related('user').prefetch_related(
            'post_comments',
            'post_likes',
            'post_audios',
            'post_images',
            'post_videos'
        ).annotate(
            likes_count=Count('post_likes', distinct=True),
            comments_count=Count('post_comments', distinct=True)
        ).all()
