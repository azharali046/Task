from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import  APITestCase


class RegAPITes(APITestCase):
    client = Client()

    def test_user_tweets(self):
        kwargs = {'user':'azhar'}
        response = self.client.get(reverse('get-user-tweets', kwargs=kwargs), format='json' )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hashtags_tweets(self):
        kwargs ={'hashtag':'HASHTAG'}
        response = self.client.get(reverse('get-hashtag-tweets', kwargs=kwargs), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)