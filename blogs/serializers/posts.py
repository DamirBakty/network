from rest_framework import serializers

from blogs.models.posts import Post, PostImage, PostVideo, PostAudio, PostLike


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ('id', 'image')


class PostVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideo
        fields = ('id', 'video')


class PostAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAudio
        fields = ('id', 'audio')


class PostListSerializer(serializers.ModelSerializer):
    post_images = PostImageSerializer(many=True, required=False)
    post_audios = PostAudioSerializer(many=True, required=False)
    post_videos = PostVideoSerializer(many=True, required=False)
    yours = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
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
        liked = PostLike.objects.filter(post=obj, user=user)
        return True if liked else False


class ImageCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = PostImage
        fields = ('image',)


class AudioCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostAudio
        fields = ('audio',)


class VideoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostVideo
        fields = ('video',)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text')
