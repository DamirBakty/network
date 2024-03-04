from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models.posts import Post, PostLike, PostAudio, PostImage, PostVideo, Postmark

User = get_user_model()

class PostModelAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/posts/'
        self.user = User.objects.create_user(email='testuser@mail.ru', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_get_all_objects(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_object(self):
        data = {"title": "test title", "text": "test text"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_authenticated_user_can_create_object(self):
        data = {"title": "test title", "text": "test text"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
