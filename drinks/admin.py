from django.contrib import admin
from .models import Cocktail
# Register your models here.

class CocktailAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cocktail, CocktailAdmin)
