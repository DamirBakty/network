import rest_framework.permissions
from rest_framework import generics
from rest_framework.views import APIView

from blogs import serializers, services, permissions
from rest_framework.response import Response
from rest_framework import status
import collections

class PostListCreateAPIView(generics.ListCreateAPIView):
    post_service: services.PostListCreateServiceInterface = services.PostListCreateServiceV1()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.PostCreateSerializer
        return serializers.PostListSerializer

    def perform_create(self, serializer):
        post_create_serializer = self.get_serializer(data=self.request.data)
        post_create_serializer.is_valid(raise_exception=True)
        data = collections.OrderedDict({
            'post': post_create_serializer.validated_data,
            'user': self.request.user,
        })
        if 'image' in self.request.data:
            images = [{'image': i} for i in dict(self.request.data).pop('image')]
            image_create_serializer = serializers.ImageCreateSerializer(data=images, many=True)
            image_create_serializer.is_valid(raise_exception=True)
            data.update({
                'image': image_create_serializer.validated_data
            })
        if 'audio' in self.request.data:
            audio = [{'audio': i} for i in dict(self.request.data).pop('audio')]
            audio_create_serializer = serializers.AudioCreateSerializer(data=audio, many=True)
            audio_create_serializer.is_valid(raise_exception=True)
            data.update({
                'audio': audio_create_serializer.validated_data
            })
        if 'video' in self.request.data:
            videos = [{'video': v} for v in dict(self.request.data).pop('video')]
            video_create_serializer = serializers.VideoCreateSerializer(data=videos, many=True)
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
    post_service: services.PostGetUpdateDeleteServiceInterface = services.PostGetUpdateDeleteServiceV1()
    permission_classes = [rest_framework.permissions.IsAuthenticated, permissions.PostPermission]
    serializer_class = serializers.PostListSerializer
    lookup_field = 'pk'

    def get_object(self):
        return self.post_service.get_post(pk=self.kwargs['pk'])


class PostLikeAPIView(APIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    post_service: services.PostGetUpdateDeleteServiceInterface = services.PostGetUpdateDeleteServiceV1()

    def get(self, request, pk):
        return Response(self.post_service.like_post(post_id=pk, user=request.user))


class CommentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    comment_service: services.CommentListCreateServiceInterface = services.CommentListCreateServiceV1()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CommentCreateSerializer
        return serializers.CommentListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return self.comment_service.get_comments(post_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        comment_serializer = self.get_serializer(data=self.request.data)
        comment_serializer.is_valid(raise_exception=True)
        data = collections.OrderedDict({
            'comment': comment_serializer.validated_data,
            'user': self.request.user
        })
        self.comment_service.create_comment(post_id=self.kwargs['pk'], data=data)

# class CommentLikeAPIView(APIView):
#     permission_classes =
