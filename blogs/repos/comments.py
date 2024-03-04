from typing import Protocol, OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from rest_framework.generics import get_object_or_404

from blogs.models.comments import CommentLike, Comment
from blogs.models.posts import Post


class CommentListCreateReposInterface(Protocol):
    @staticmethod
    def get_comments(post_id: int): ...

    @staticmethod
    def create_comment(post_id: int, data: OrderedDict): ...


class CommentGetUpdateDeleteReposInterface(Protocol):
    @staticmethod
    def get_comment(pk: int): ...

    @staticmethod
    def like_comment(pk: int, user): ...


class CommentListCreateReposV1:
    @staticmethod
    def get_comments(post_id: int):
        comments = Comment.objects.select_related('user').prefetch_related(
            'comment_likes'
        ).annotate(
            likes_count=Count('comment_likes', distinct=True)
        ).filter(post_id=post_id)
        return comments

    @staticmethod
    def create_comment(post_id: int, data: OrderedDict):
        try:
            user = data.pop('user')
            post = Post.objects.get(id=post_id)
            comment_data = data.pop('comment')
            comment = Comment.objects.create(**comment_data, post=post, user=user)
            return comment
        except ObjectDoesNotExist:
            return ValueError("Post does not exist")


class CommentGetUpdateDeleteReposV1:
    @staticmethod
    def get_comment(pk: int):
        comment = get_object_or_404(
            Comment.objects.select_related('user').prefetch_related(
                'comment_likes'
            ).annotate(
                likes_count=Count('comment_likes', distinct=True)
            ), pk=pk)
        return comment

    @staticmethod
    def like_comment(comment_id: int, user):
        obj, liked = CommentLike.objects.get_or_create(comment_id=comment_id, user=user)
        if not liked:
            obj.delete()
        likes_count = CommentLike.objects.filter(comment_id=comment_id).count()
        return {'liked': liked, 'likes_count': likes_count}
