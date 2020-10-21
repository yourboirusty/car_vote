from rest_framework import serializers
from api.models import Car, Review


class ReviewedCarSerializer(serializers.ModelSerializer):
    average_rating = serializers.DecimalField(max_digits=2,
                                              decimal_places=1,
                                              read_only=True)

    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'average_rating')
        read_only_fields = ('id', 'average_rating')

    def validate(self, attrs):
        instance = Car(**attrs)
        instance.clean()
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('car', 'review')
