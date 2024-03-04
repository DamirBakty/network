from django.contrib import admin
from blogs.models.comments import Comment, CommentLike
from blogs.models.posts import Post, PostImage, PostAudio, PostVideo, PostLike, Postmark

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostImage)
admin.site.register(PostAudio)
admin.site.register(PostVideo)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Postmark)
