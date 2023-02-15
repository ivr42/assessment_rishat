from django.contrib import admin

from .models import Item


@admin.register(Item)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    list_display_links = ("id", "name", "price")
    search_fields = ("name",)
