from rest_framework import serializers
from blogs.models.comments import Comment, CommentLike


class CommentListSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField()
    liked = serializers.SerializerMethodField()
    yours = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
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
        liked = CommentLike.objects.filter(comment=obj, user=user)
        return True if liked else False


class CommentCreateUpdateSerializer(serializers.Serializer):
    text = serializers.CharField()
