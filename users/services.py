from typing import Protocol, OrderedDict

from django.core.mail import send_mail

from network import settings
from . import repos
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class UserServicesInterface(Protocol):
    def create_user(self, data: OrderedDict): ...

    def verify_email(self, data: OrderedDict): ...

    def generate_token(self, data: OrderedDict, request): ...


class UserServiceV1:
    user_repos: repos.UserReposInterface = repos.UserReposV1()

    def create_user(self, data: OrderedDict):
        user = self.user_repos.create_user(data)
        pk = user.pk
        token = default_token_generator.make_token(user)
        uid = force_str(urlsafe_base64_encode(force_bytes(pk)))
        sent = self._send_message_to_email(email=user.email,
                                           token=token,
                                           uid=uid)
        return sent

    def verify_email(self, data: OrderedDict):
        pk = force_str(urlsafe_base64_decode(data['uid']))
        token = data['token']
        user = self.user_repos.get_user(pk=pk)
        if default_token_generator.check_token(user, token):
            self.user_repos.activate_user(user)
            return True
        return False

    def generate_token(self, data: OrderedDict, request):
        user = self.user_repos.authenticate_user(data=data, request=request)
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        data = {
            'access_token': str(access_token),
            'refresh_token': str(refresh_token),
        }
        return data

    @staticmethod
    def _send_message_to_email(email: str, token, uid):
        data = {
            'token': token,
            'uid': uid
        }
        send_mail(
            subject='Subject',
            message=str(data),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        return True
