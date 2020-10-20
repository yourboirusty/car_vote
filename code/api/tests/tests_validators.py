from django.test import TestCase
from django.core.exceptions import ValidationError
from api.validators import validate_car


class CarValidatorTestCase(TestCase):
    def setUp(self):
        self.real_car = {'make': 'HoNDa',
                         'model': 'cIVic'}
        self.fake_car = {'make': 'Lambordiginio',
                         'model': 'VroomVroom'}

    def test_correct_car(self):
        result = validate_car(**self.real_car)
        self.assertEqual(result[0].lower(),
                         self.real_car['make'].lower())
        self.assertEqual(result[1].lower(),
                         self.real_car['model'].lower())

    def test_incorrect_maker(self):
        errormsg = "No models found for " + self.fake_car['make']
        with self.assertRaisesMessage(ValidationError, errormsg):
            validate_car(**self.fake_car)

    def test_incorrect_model(self):
        errormsg = "Maker has no model " + self.fake_car['model']
        with self.assertRaisesMessage(ValidationError, errormsg):
            validate_car(self.real_car['make'], self.fake_car['model'])

    def test_case_correction(self):
        result = validate_car(**self.real_car)
        self.assertEqual(result[0], 'HONDA')
        self.assertEqual(result[1], "Civic")
