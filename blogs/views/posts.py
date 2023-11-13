import collections

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs.serializers.posts import ImageCreateSerializer, AudioCreateSerializer, VideoCreateSerializer, \
    PostListSerializer, PostCreateSerializer
from blogs.services.posts import PostListCreateServiceInterface, PostListCreateServiceV1, \
    PostGetUpdateDeleteServiceInterface, PostGetUpdateDeleteServiceV1


class PostListCreateAPIView(generics.ListCreateAPIView):
    post_service: PostListCreateServiceInterface = PostListCreateServiceV1()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'id', 'text']
    search_fields = ['=user__username']
    ordering_fields = ['created_at', 'updated_at', 'likes_count']


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        post_create_serializer = self.get_serializer(data=self.request.data)
        post_create_serializer.is_valid(raise_exception=True)
        data = collections.OrderedDict({
            'post': post_create_serializer.validated_data,
            'user': self.request.user,
        })
        if 'image' in self.request.data:
            images = [{'image': i} for i in dict(self.request.data).pop('image')]
            image_create_serializer = ImageCreateSerializer(data=images, many=True)
            image_create_serializer.is_valid(raise_exception=True)
            data.update({
                'image': image_create_serializer.validated_data
            })
        if 'audio' in self.request.data:
            audio = [{'audio': i} for i in dict(self.request.data).pop('audio')]
            audio_create_serializer = AudioCreateSerializer(data=audio, many=True)
            audio_create_serializer.is_valid(raise_exception=True)
            data.update({
                'audio': audio_create_serializer.validated_data
            })
        if 'video' in self.request.data:
            videos = [{'video': v} for v in dict(self.request.data).pop('video')]
            video_create_serializer = VideoCreateSerializer(data=videos, many=True)
            video_create_serializer.is_valid(raise_exception=True)
            data.update({
                'video': video_create_serializer.validated_data
            })

        self.post_service.create_post(data=data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {'message': 'Post created successfully'}
        return Response(response_data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return self.post_service.get_posts()


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    post_service: PostGetUpdateDeleteServiceInterface = PostGetUpdateDeleteServiceV1()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostListSerializer
    lookup_field = 'pk'

    def get_object(self):
        if self.request.method == "GET":
            return self.post_service.get_post(pk=self.kwargs[self.lookup_field])
        return self.post_service.get_post(pk=self.kwargs[self.lookup_field], user=self.request.user)


class PostLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    post_service: PostGetUpdateDeleteServiceInterface = PostGetUpdateDeleteServiceV1()

    def get(self, request, pk):
        return Response(self.post_service.like_post(post_id=pk, user=request.user))

class PostMarkAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    post_service: PostGetUpdateDeleteServiceInterface = PostGetUpdateDeleteServiceV1()

    def get(self, request, pk):
        return Response(self.post_service.mark_post(post_id=pk, user=request.user))
