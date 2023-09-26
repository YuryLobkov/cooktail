from rest_framework import serializers
from drinks.models import Cocktail, Ingredients, Inventory, GroupsCocktail


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['name', 'ing_type', 'descriprion']


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['name', 'inv_type']

class DrinkSerializer(serializers.ModelSerializer):
    date_posted = serializers.ReadOnlyField()
    group = serializers.SlugRelatedField(
        many=False, queryset=GroupsCocktail.objects.all(), slug_field='group_name')
    main_ingredients = serializers.SlugRelatedField(
        many=True, queryset=Ingredients.objects.all(), slug_field='name')
    optional_ingredients = serializers.SlugRelatedField(
        many=True, queryset=Ingredients.objects.all(), slug_field='name')
    tools = serializers.SlugRelatedField(
        many=True, queryset=Inventory.objects.all(), slug_field='name')

    class Meta:
        model = Cocktail
        fields = ['id', 'name', 'group', 'volume', 'main_ingredients',
                  'optional_ingredients', 'tools', 'recepie', 'image', 'user_id', 'date_posted']


class DrinkCreateSerializer(serializers.ModelSerializer):
    date_posted = serializers.ReadOnlyField()
    group = serializers.PrimaryKeyRelatedField(
        many=False, queryset=GroupsCocktail.objects.all())
    main_ingredients = IngredientSerializer
    optional_ingredients = IngredientSerializer
    tools = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Inventory.objects.all())

    class Meta:
        model = Cocktail
        fields = ['id', 'name', 'group', 'volume', 'main_ingredients',
                  'optional_ingredients', 'tools', 'recepie', 'image', 'user_id', 'date_posted']
        
    # def create(self, validated_data):
    #     profile_data = validated_data.pop('main')
    #     user = User.objects.create(**validated_data)
    #     Profile.objects.create(user=user, **profile_data)
    #     return user
