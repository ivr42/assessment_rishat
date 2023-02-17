from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from shop.models import Item

from .serializers import BuySerializer, ItemWithStripeSerializer


class BuyView(RetrieveAPIView):
    serializer_class = BuySerializer
    queryset = Item.objects.all()


class ItemView(RetrieveAPIView):
    serializer_class = ItemWithStripeSerializer
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer({"item": self.get_object()})
        return Response(
            serializer.data,
            template_name="item.html",
        )
