from django.contrib import admin
from .models import Cocktail, GroupsCocktail, Ingredients, Inventory
# Register your models here.

class CocktailAdmin(admin.ModelAdmin):
    pass
class CocktailGroupAdmin(admin.ModelAdmin):
    pass
class IngredientsAdmin(admin.ModelAdmin):
    pass
class InventoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cocktail, CocktailAdmin)
admin.site.register(GroupsCocktail, CocktailGroupAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Inventory, InventoryAdmin)
