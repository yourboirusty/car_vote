from rest_framework import generics
from rest_framework.response import Response
from api.models import Car, Review
from api.serializers import ReviewSerializer, ReviewedCarSerializer


class ListCreateCars(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = ReviewedCarSerializer


class ListPopularCars(generics.ListAPIView):
    queryset = Car.most_popular()
    serializer_class = ReviewedCarSerializer


class CreateReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
