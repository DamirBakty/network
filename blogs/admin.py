from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.PostImage)
admin.site.register(models.PostAudio)
admin.site.register(models.PostVideo)
admin.site.register(models.PostLike)
admin.site.register(models.CommentLike)
admin.site.register(models.Postmark)
