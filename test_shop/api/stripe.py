from urllib.parse import urlparse

import stripe
from django.conf import settings
from pydantic import BaseModel, PositiveInt
from shop.models import Item


class ProductData(BaseModel):
    name: str
    description: str


class PriceData(BaseModel):
    product_data: ProductData
    currency: str
    unit_amount_decimal: PositiveInt


class ProductItem(BaseModel):
    price_data: PriceData
    quantity: PositiveInt


def _make_static_uri(full_path: str, new_path: str) -> str:
    """Makes new URI from full_path by replacing path and removing the rest

    Args:
        full_path: uri, got for example with `reverse` DRF function
        new_path: a new path to be used for replacement path in URI

    Returns:
        a new URI
    """
    parsed_full_path = urlparse(full_path)
    return (
        f"{parsed_full_path.scheme}://{parsed_full_path.netloc}"
        f"{settings.STATIC_URL}"
        f"{new_path.lstrip('/')}"
    )


def stripe_session_fabric(obj: Item, endpoint: str) -> stripe.checkout.Session:
    """Initiate a stripe checkout session

    Args:
        obj: an Item instance
        endpoint: full URI to endpoint, used to produce
            success and cancel pages URIs needed by stripe API.

    Returns:
        stripe checkout session
    """
    stripe.api_key = settings.STRIPE["STRIPE_SECRET_KEY"]

    product_obj = ProductItem(
        price_data=PriceData(
            product_data=ProductData(
                name=obj.name,
                description=obj.description,
            ),
            currency=settings.STRIPE["CURRENCY"],
            unit_amount_decimal=obj.price * 100,
        ),
        quantity=1,
    )

    stripe_session = stripe.checkout.Session.create(
        line_items=[product_obj.dict()],
        mode="payment",
        success_url=_make_static_uri(endpoint, settings.STRIPE["SUCCESS_PAGE"]),
        cancel_url=endpoint,
    )

    return stripe_session


def get_stripe_session_id(*args, **kwargs) -> str:
    return stripe_session_fabric(*args, **kwargs).stripe_id
