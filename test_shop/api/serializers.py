from rest_framework import serializers

from shop.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "price", "description")


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "price", "description")
