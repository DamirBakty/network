from rest_framework import serializers
from blogs import models


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
        model = models.PostAudio
        fields = ('id', 'audio')


class PostListSerializer(serializers.ModelSerializer):
    post_images = PostImageSerializer(many=True, required=False)
    post_audios = PostAudioSerializer(many=True, required=False)
    post_videos = PostVideoSerializer(many=True, required=False)
    yours = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = (
            'id',
            'title',
            'text',
            'updated_at',
            'post_images',
            'post_videos',
            'post_audios',
            'yours',
            'author_name',
            'likes_count',
            'comments_count',
            'liked'
        )

    def get_yours(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return True if user == obj.user else False

    @staticmethod
    def get_author_name(obj):
        return str(obj.user)

    def get_liked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        liked = models.PostLike.objects.filter(post=obj, user=user)
        return True if liked else False


class CommentListSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField()
    liked = serializers.SerializerMethodField()
    yours = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'text',
            'updated_at',
            'likes_count',
            'liked',
            'yours',
            'author_name'
        )

    def get_yours(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return True if user == obj.user else False

    @staticmethod
    def get_author_name(obj):
        return str(obj.user)

    def get_liked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        liked = models.CommentLike.objects.filter(comment=obj, user=user)
        return True if liked else False


class ImageCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = models.PostImage
        fields = ('image',)


class AudioCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PostAudio
        fields = ('audio',)


class VideoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PostVideo
        fields = ('video',)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('title', 'text')


class CommentCreateSerializer(serializers.Serializer):
    text = serializers.CharField()
