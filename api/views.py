from rest_framework import generics
from .serializers import DrinkSerializer
from drinks.models import Cocktail

class Drinks(generics.ListAPIView):
    serializer_class = DrinkSerializer

    def get_queryset(self):
        return Cocktail.objects.all()