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
