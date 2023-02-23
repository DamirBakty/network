from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from . import models, serializers, services
from rest_framework.viewsets import ViewSet



class UserViewSet(ViewSet):
    model = models.User
    user_services: services.UserServicesInterface = services.UserServiceV1()
    permission_classes = []

    @action(detail=False, permission_classes=[permissions.AllowAny])
    def create_user(self, request, *args, **kwargs):
        serializer = serializers.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sent = self.user_services.create_user(data=serializer.validated_data)

        return Response({"Sent": sent})

    @action(detail=False, permission_classes=[permissions.AllowAny])
    def verify_email(self, request):
        serializer = serializers.VerifyUserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verified = self.user_services.verify_email(data=serializer.validated_data)
        return Response({"Verified": verified})

    @action(detail=False, permission_classes=[permissions.AllowAny])
    def generate_token(self, request):
        serializer = serializers.LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = self.user_services.generate_token(data=serializer.validated_data, request=request)
        return Response(response_data)



