from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Review, Car
from django.db.utils import IntegrityError

client = APIClient()


class CarsEndpointTestCase(TestCase):
    def setUp(self):
        self.url = reverse('api.cars')
        self.cars = [
            Car(make='Honda', model='Civic'),
            Car(make='Mercedes', model='Sprinter'),
            Car(make='Tesla', model='Roadster'),
            Car(make='Volvo', model='S60'),
            Car(make='Volkswagen', model='Golf'),
            Car(make='Volkswagen', model='Jetta')
        ]
        for car in self.cars:
            car.save()
            Review.objects.create(car=car, review=4)

    def test_post_wrong_car_make(self):
        response = client.post(self.url,
                               {'make': 'asdf',
                                'model': 'Golf'}
                               )
        self.assertEqual(response.status_code, 400)

    def test_post_wrong_car_model(self):
        response = client.post(self.url,
                               {'make': 'Volkswagen',
                                'model': 'Flammenwerfer'}
                               )
        self.assertEqual(response.status_code, 400)

    def test_post_duplicate_car(self):
        with self.assertRaises(IntegrityError):
            client.post(self.url,
                        {'make': 'honda',
                         'model': 'Civic'}
                        )

    def test_post_code(self):
        response = client.post(self.url,
                               {'make': 'honda',
                                'model': 'accord'}
                               )
        self.assertEqual(response.status_code, 201)

    def test_post_data(self):
        response = client.post(self.url,
                               {'make': 'honda',
                                'model': 'accord'}
                               )
        data = response.data

        self.assertIsNotNone(data['id'])
        self.assertEqual(data['make'], 'HONDA')
        self.assertEqual(data['model'], 'Accord')

    def test_get_code(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_data(self):
        response = client.get(self.url)
        data = response.data
        self.assertEqual(data['count'], len(self.cars))
        self.assertCountEqual(
            data['results'][0].keys(),
            ['id', 'make', 'model', 'average_rating']
        )
        self.assertEqual(data['results'][0]['average_rating'], '4.0')
        self.assertEqual(data['results'][0]['make'], 'HONDA')
        self.assertEqual(data['results'][0]['model'], 'Civic')

    def test_put_code(self):
        response = client.put(self.url)
        self.assertEqual(response.status_code, 405)

    def test_delete_code(self):
        response = client.delete(self.url)
        self.assertEqual(response.status_code, 405)
