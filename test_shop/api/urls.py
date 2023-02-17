from django.urls import include, path
from rest_framework import routers

from .views import BuyView, ItemView

api_router = routers.DefaultRouter()

urlpatterns = [
    path("", include(api_router.urls)),
    path("item/<pk>/", ItemView.as_view(), name="api_item"),
    path("buy/<pk>/", BuyView.as_view(), name="api_buy"),
]
