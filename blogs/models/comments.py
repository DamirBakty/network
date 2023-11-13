from django.contrib.auth import get_user_model
from django.db import models

from blogs.models.posts import Post


class Comment(models.Model):
    text = models.TextField(verbose_name='Text')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_comments',
        verbose_name='Post'
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Author'
    )


class CommentLike(models.Model):
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE,
        related_name='comment_likes',
        verbose_name='Comment'
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Author'
    )
