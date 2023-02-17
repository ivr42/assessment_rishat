from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse
from shop.models import Item

from .stripe import get_stripe_session_id


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "price", "description")


class ItemWithStripeSerializer(serializers.Serializer):
    item = ItemSerializer()
    stripe_public_key = serializers.SerializerMethodField()

    class Meta:
        fields = ("item", "stripe_public_key")

    def get_stripe_public_key(self, obj):
        return settings.STRIPE["STRIPE_PUBLIC_KEY"]


class BuySerializer(serializers.ModelSerializer):
    session_id = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ("session_id",)

    def get_session_id(self, obj):
        return get_stripe_session_id(
            reverse("api_item", str(obj.id), request=self.context["request"]),
            obj,
        )
