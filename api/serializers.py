from rest_framework import serializers
from drinks.models import Cocktail

class DrinkSerializer(serializers.ModelSerializer):
    date_posted = serializers.ReadOnlyField()

    class Meta:
        model = Cocktail
        fields = ['id', 'name', 'group', 'volume', 'main_ingredients', 'optional_ingredients', 'tools', 'recepie', 'image', 'user_id', 'date_posted']