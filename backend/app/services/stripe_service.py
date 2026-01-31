import stripe

from ..core.config import settings



stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(
    email: str,
    success_url: str,
    cancel_url: str,
    metadata: dict
):
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        customer_email=email,
        line_items=[
            {
                "price": settings.STRIPE_PRICE_ID,
                "quantity": 1,
            }
        ],
        metadata=metadata,
        success_url=success_url,
        cancel_url=cancel_url,
    )


def verify_webhook(payload, sig_header):
    return stripe.Webhook.construct_event(
        payload=payload,
        sig_header=sig_header,
        secret=settings.STRIPE_WEBHOOK_SECRET
    )
