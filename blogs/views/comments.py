import collections

from rest_framework import permissions, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs.models.comments import Comment
from blogs.serializers.comments import CommentCreateUpdateSerializer, CommentListSerializer
from blogs.services.comments import CommentGetUpdateDeleteServiceInterface, CommentGetUpdateDeleteServiceV1, \
    CommentListCreateServiceInterface, CommentListCreateServiceV1


class CommentLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    comment_service: CommentGetUpdateDeleteServiceInterface = CommentGetUpdateDeleteServiceV1()

    def get(self, request, pk):
        return Response(self.comment_service.like_comment(pk=pk, user=request.user))


class CommentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    comment_service: CommentListCreateServiceInterface = CommentListCreateServiceV1()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateUpdateSerializer
        return CommentListSerializer

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


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentListSerializer
        return CommentCreateUpdateSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), self.kwargs[self.lookup_field])
