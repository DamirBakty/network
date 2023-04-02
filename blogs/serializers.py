from rest_framework import serializers
from blogs import models
from django.contrib.auth import get_user_model


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PostImage
        fields = ('id', 'image')


class PostVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostVideo
        fields = ('id', 'video')


class PostAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostVideo
        fields = ('id', 'video')

class PostSerializer(serializers.ModelSerializer):
    post_images = PostImageSerializer(many=True, required=False)
    post_audios = PostAudioSerializer(many=True, required=False)
    post_videos = PostVideoSerializer(many=True, required=False)
    yours = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()

    class Meta:
        model = models.Post
        fields = ('id', 'title', 'text', 'updated_at', 'post_images', 'post_videos', 'post_audios', 'yours', 'author_name', 'likes_count', 'comments_count')


    def get_yours(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return True if user == obj.user else False

    def get_author_name(self, obj):
        return str(obj.user)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('title', 'text')
