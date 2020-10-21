from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import Car, Review


class CarModelTestCase(TestCase):
    def setUp(self):
        self.car = Car(make='Honda', model='Civic')

    def test_car_creation(self):
        self.car.full_clean()
        self.car.save()
        self.assertIsNotNone(self.car.id)

    def test_car_make_validation(self):
        with self.assertRaises(ValidationError):
            self.car.model = "VroomVroom"
            self.car.full_clean()

    def test_car_model_validation(self):
        with self.assertRaises(ValidationError):
            self.car.make = "Lambordigini"
            self.car.full_clean()

    def test_case_correction(self):
        self.car = Car(make='HoNDA', model='ciVic')
        self.car.save()
        self.car.full_clean()
        self.car.refresh_from_db()
        self.assertEqual(self.car.make, 'HONDA')
        self.assertEqual(self.car.model, 'Civic')


class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.car = Car(make='Honda', model='Civic')
        self.car.save()
        self.review = Review(car=self.car, review=2)

    def test_review_creation(self):
        self.review.save()
        self.assertIsNotNone(self.review.id)

    def test_review_low_validation(self):
        with self.assertRaises(ValidationError):
            self.review.review = -10
            self.review.full_clean()

    def test_review_high_validation(self):
        with self.assertRaises(ValidationError):
            self.review.review = 10
            self.review.full_clean()


class CarReviewTestCase(TestCase):
    def setUp(self):
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

        # Create a dictionary of variable n of reviews bound to cars
        self.reviews = dict()
        for n, car in enumerate(self.cars, start=1):
            self.reviews[str(car)] = {
                'avg': 0,
                'reviews': list()
            }
            for _ in range(n):
                rate = n % 4 + 1
                review = Review(car=car, review=rate)
                review.save()
                self.reviews[str(car)]['reviews'].append(review)
                self.reviews[str(car)]['avg'] += rate
            self.reviews[str(car)]['avg'] /= n

    def test_average_rating(self):
        for car in self.cars:
            self.assertEqual(car.average_rating(),
                             self.reviews[str(car)]['avg'])

    def test_average_no_reviews(self):
        car = Car(make='Tesla', model='Model s')
        car.save()
        self.assertIsNone(car.average_rating())

    def test_review_count(self):
        for n, car in enumerate(self.cars, start=1):
            self.assertEqual(car.number_of_reviews(), n)

    def test_popular(self):
        popular = Car.most_popular()
        self.assertEqual(len(popular), 5)
        self.assertListEqual(list(popular), self.cars[:5])
        self.assertEqual(type(popular), type(Car.objects.all()))
