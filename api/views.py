from rest_framework import generics, permissions
from .serializers import DrinkSerializer, DrinkCreateSerializer
from drinks.models import Cocktail


class Drinks(generics.ListAPIView):
    serializer_class = DrinkSerializer

    def get_queryset(self):
        return Cocktail.objects.prefetch_related('main_ingredients', 'optional_ingredients', 'group', 'tools')


class DrinksCreate(generics.ListCreateAPIView):
    serializer_class = DrinkCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cocktail.objects.all()
