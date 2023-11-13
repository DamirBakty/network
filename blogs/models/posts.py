from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    text = models.TextField(verbose_name='Text')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_posts',
        verbose_name='Author'
    )

    def __str__(self):
        return f'ID: {self.id} Title: {self.title}'


class PostImage(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_images',
        verbose_name='Post'
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Author'
    )

    image = models.ImageField(upload_to='post/images', max_length=255, verbose_name='Image')


class PostVideo(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_videos',
        verbose_name='Post'
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Author'
    )

    video = models.FileField(upload_to='post/videos', max_length=255)


class PostAudio(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_audios',
        verbose_name='Post'
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Author'
    )

    audio = models.FileField(upload_to='post/audios', max_length=255)


class PostLike(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_likes',
        verbose_name='Post'
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Author'
    )


class Postmark(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_marks',
        verbose_name='Post'
    )

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Author'
    )

    created_at = models.DateTimeField(auto_now_add=True)
