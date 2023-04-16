from typing import Protocol, OrderedDict
from rest_framework.generics import get_object_or_404
from django.db import transaction
from blogs import models
from django.db.models import Count, OuterRef, Subquery, Exists
from django.core.exceptions import ObjectDoesNotExist

class PostListCreateReposInterface(Protocol):
    @staticmethod
    def create_post(data: OrderedDict): ...

    @staticmethod
    def get_posts(): ...


class PostGetUpdateDeleteReposInterface(Protocol):
    @staticmethod
    def get_post(pk): ...

    @staticmethod
    def like_post(post_id, user): ...


class CommentListCreateReposeInterface(Protocol):
    @staticmethod
    def get_comments(post_id: int): ...

    @staticmethod
    def create_comment(post_id: int, data: OrderedDict): ...


class PostGetUpdateDeleteReposV1:
    @staticmethod
    def like_post(post_id, user):
        obj, liked = models.PostLike.objects.get_or_create(post_id=post_id, user=user)
        if not liked:
            obj.delete()
        likes_count = models.PostLike.objects.filter(post_id=post_id).count()
        return {'liked': liked, 'likes_count': likes_count}

    @staticmethod
    def get_post(pk):
        post = get_object_or_404(
            models.Post.objects.select_related('user').prefetch_related(
                'post_comments',
                'post_likes',
                'post_audios',
                'post_images',
                'post_videos'
            ).annotate(
                likes_count=Count('post_likes', distinct=True),
                comments_count=Count('post_comments', distinct=True)
            ),
            pk=pk
        )
        return post


class PostListCreateReposV1:
    @staticmethod
    def create_post(data: OrderedDict):
        with transaction.atomic():
            user = data.pop('user')
            post_data = data.pop('post')
            post = models.Post.objects.create(**post_data, user=user)
            if 'image' in data:
                images = [
                    models.PostImage(
                        user=user,
                        image=i['image'],
                        post=post
                    ) for i in data.pop('image')
                ]
                models.PostImage.objects.bulk_create(images)
            if 'audio' in data:
                audios = [
                    models.PostAudio(
                        user=user,
                        audio=i['audio'],
                        post=post
                    ) for i in data.pop('audio')
                ]
                models.PostAudio.objects.bulk_create(audios)
            if 'video' in data:
                videos = [
                    models.PostVideo(
                        user=user,
                        video=i['video'],
                        post=post
                    ) for i in data.pop('video')
                ]
                models.PostVideo.objects.bulk_create(videos)

    @staticmethod
    def get_posts():
        return models.Post.objects.select_related('user').prefetch_related(
            'post_comments',
            'post_likes',
            'post_audios',
            'post_images',
            'post_videos'
        ).annotate(
            likes_count=Count('post_likes', distinct=True),
            comments_count=Count('post_comments', distinct=True)
        )


class CommentListCreateReposV1:
    @staticmethod
    def get_comments(post_id: int):
        comments = models.Comment.objects.select_related('user').prefetch_related(
            'comment_likes'
        ).annotate(
            likes_count=Count('comment_likes', distinct=True)
        ).filter(post_id=post_id)
        return comments

    @staticmethod
    def create_comment(post_id: int, data: OrderedDict):
        try:
            user = data.pop('user')
            post = models.Post.objects.get(id=post_id)
            comment_data = data.pop('comment')
            comment = models.Comment.objects.create(**comment_data, post=post, user=user)
            return comment
        except ObjectDoesNotExist:
            return ValueError("Post does not exist")
