from urllib.parse import urlparse

import stripe
from django.conf import settings
from shop.models import Item


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


def get_stripe_session(
    endpoint: str, product: Item
) -> stripe.checkout.Session:
    """Initiate a stripe checkout session

    Args:
        endpoint: full URI to endpoint, used to produce
            success and cancel pages URIs needed by stripe API.
        product: an Item instance

    Returns:
        stripe checkout session
    """
    stripe.api_key = settings.STRIPE["STRIPE_SECRET_KEY"]

    items = [
        {
            "price_data": {
                "currency": settings.STRIPE["CURRENCY"],
                "product_data": {
                    "name": product.name,
                    "description": product.description,
                },
                "unit_amount_decimal": int(product.price * 100),
            },
            "quantity": 1,
        },
    ]

    stripe_session = stripe.checkout.Session.create(
        line_items=items,
        mode="payment",
        success_url=_make_static_uri(
            endpoint, settings.STRIPE["SUCCESS_PAGE"]
        ),
        cancel_url=endpoint,
    )

    return stripe_session


def get_stripe_session_id(*args, **kwargs) -> str:
    return get_stripe_session(*args, **kwargs).stripe_id
