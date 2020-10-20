from django.core.exceptions import ValidationError
import urllib.request
import json
from typing import Tuple


def validate_car(make: str, model: str) -> Tuple[str, str]:
    """Validate if car exists via https://vpic.nhtsa.dot.gov/api/.
    Ignores letter casing.
    Returns car make and model with proper casing.
    """

    make_models = urllib.request.urlopen(
        "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/"
        + make + "?format=json"
        ).read()
    make_models = json.loads(make_models)
    model_lower = model.lower()

    if make_models.get('Count') == 0:
        raise ValidationError("No models found for " + make)

    models_filtered = list(filter(
        lambda car: car.get('Model_Name').lower() == model_lower,
        make_models.get('Results')
        ))

    if not len(models_filtered):
        raise ValidationError("Maker has no model " + model)

    [car] = models_filtered

    return (car.get('Make_Name'), car.get('Model_Name'))
