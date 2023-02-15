from django.urls import include, path
from rest_framework import routers

from .views import ItemView, return_stripe_session_id

api_router = routers.DefaultRouter()

urlpatterns = [
    path("", include(api_router.urls)),
    path("buy/<pk>/", return_stripe_session_id, name="api_buy"),
    path("item/<pk>/", ItemView.as_view(), name="api_item"),
]
