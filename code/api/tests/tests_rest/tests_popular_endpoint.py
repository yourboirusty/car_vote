from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Car, Review

client = APIClient()


class PopularEndpointTestCase(TestCase):
    def setUp(self):
        self.url = reverse('api.popular')
        # Create list of cars and save them
        self.cars = [
            Car(make='Honda', model='Civic'),
            Car(make='Mercedes', model='Sprinter'),
            Car(make='Tesla', model='Roadster'),
            Car(make='Volvo', model='S60'),
            Car(make='Volkswagen', model='Golf'),
            Car(make='Volkswagen', model='Jetta')
        ]
        [car.save() for car in self.cars]

        # Make sure list isn't sorted by ids
        self.cars.reverse()

        # Create a dictionary of variable n of reviews bound to cars
        self.reviews = dict()
        for n, car in enumerate(self.cars, start=1):
            self.reviews[str(car)] = {
                'avg': 0,
                'reviews': list()
            }
            for _ in range(1, n):
                rate = 6-n
                review = Review(car=car, review=rate)
                review.save()
                self.reviews[str(car)]['reviews'].append(review)
                self.reviews[str(car)]['avg'] += rate
            self.reviews[str(car)]['avg'] /= n

    def test_get_code(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_data(self):
        response = client.get(self.url)
        count = response.data['count']
        cars = response.data['results']
        self.assertEqual(count, 5)
        for (response_car, given_car) in zip(cars, self.cars):
            self.assertEqual(response_car['id'], given_car.id)
