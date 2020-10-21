from django.test import TestCase
from api.serializers import ReviewedCarSerializer, ReviewSerializer
from api.models import Car, Review


class ReviewedCarSerializerTestCase(TestCase):
    def setUp(self):
        self.car_attributes = {
            'make': 'honda',
            'model': 'civic'
        }

        self.car = Car.objects.create(**self.car_attributes)
        self.reviews = [Review.objects.create(car=self.car, review=n % 4 + 1)
                        for n in range(1, 7)]
        self.serializer = ReviewedCarSerializer(instance=self.car)

    def test_contains_expected_fields(self):
        self.assertCountEqual(
            self.serializer.data.keys(),
            ['id', 'make', 'model', 'average_rating']
        )

    def test_validation(self):
        self.car_attributes['make'] = 'Lambordiginio'
        serializer = ReviewedCarSerializer(data=self.car_attributes)
        self.assertFalse(serializer.is_valid())

    def test_average_rating(self):
        self.assertAlmostEqual(
            float(self.serializer.data['average_rating']),
            self.car.average_rating(),
            places=1
        )


class ReviewSerializerTestCase(TestCase):
    def setUp(self):
        self.car = Car.objects.create(make='honda', model='civic')
        self.review_data = {
            'car': self.car.id,
            'review': 5
        }
        self.review = Review.objects.create(car=self.car, review=5)
        self.serializer = ReviewSerializer(instance=self.review)

    def test_contains_expected_fields(self):
        self.assertCountEqual(
            self.serializer.data.keys(),
            ['car', 'review']
        )

    def test_validation(self):
        self.review_data['review'] = 6
        serializer = ReviewSerializer(data=self.review_data)
        self.assertFalse(serializer.is_valid())
