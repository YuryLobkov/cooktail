from rest_framework import serializers
from drinks.models import Cocktail


class DrinkSerializer(serializers.ModelSerializer):
    date_posted = serializers.ReadOnlyField()
    group = serializers.StringRelatedField()
    main_ingredients = serializers.StringRelatedField(many=True)
    optional_ingredients = serializers.StringRelatedField(many=True)
    tools = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cocktail
        fields = ['id', 'name', 'group', 'volume', 'main_ingredients',
                  'optional_ingredients', 'tools', 'recepie', 'image', 'user_id', 'date_posted']
