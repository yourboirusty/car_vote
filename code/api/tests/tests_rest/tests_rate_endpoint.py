from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Car

client = APIClient()


class ReviewEndpointTestCase(TestCase):
    def setUp(self):
        self.url = reverse('api.rate')
        self.car = Car.objects.create(make='Honda', model='Civic')

    def test_get_code(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_post_code(self):
        response = client.post(self.url,
                               {
                                   'car': self.car.id,
                                   'review': 2
                               })
        self.assertEqual(response.status_code, 201)

    def test_post_data(self):
        response = client.post(self.url,
                               {
                                   'car': self.car.id,
                                   'review': 2
                               })
        self.assertIsNotNone(response.data['car'])
        self.assertIsNotNone(response.data['review'])
