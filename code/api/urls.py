from django.urls import path
from api.views import ListCreateCars, ListPopularCars, CreateReview

urlpatterns = [
    path('cars/', ListCreateCars.as_view(), name='api.cars'),
    path('rate/', CreateReview.as_view(), name='api.rate'),
    path('popular/', ListPopularCars.as_view(), name='api.popular')
]