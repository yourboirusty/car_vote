from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.validators import validate_car
from django.utils.translation import gettext_lazy as _


class Car(models.Model):
    """Car model that holds a make and model.
    Validates and replaces `make` and `model` fields
    using :validators:`api.validate_car`
    """
    make = models.CharField(_("Car make name"), max_length=64)
    model = models.CharField(_("Model name"), max_length=64)

    def clean(self):
        self.make, self.model = validate_car(self.make, self.model)


class Review(models.Model):
    """Review model for :models:`api.Car`.
    Validates `review` to check if value is between 1 and 5.
    """
    car = models.ForeignKey(Car,
                            on_delete=models.CASCADE,
                            related_name="reviews")
    review = models.IntegerField(_("Rating from 1 to 5"),
                                 validators=[
                                     MinValueValidator(1),
                                     MaxValueValidator(5)
                                 ]
                                 )
