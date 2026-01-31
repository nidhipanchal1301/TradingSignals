import uuid
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_current_user
from ..database.db import get_db
from ..services.stripe_service import create_checkout_session, verify_webhook
from ..models.user import User
from ..models.subscription import Subscription



router = APIRouter(prefix="/billing", tags=["billing"])

SUCCESS_URL = "http://localhost:3000/dashboard?success=true"
CANCEL_URL = "http://localhost:3000/dashboard?canceled=true"



@router.post("/create-checkout")
def create_checkout(
    current_user: User = Depends(get_current_user),
):
    session = create_checkout_session(
        email=current_user.email,
        success_url=SUCCESS_URL,
        cancel_url=CANCEL_URL,
        metadata={
            "user_id": str(current_user.id)
        }
    )

    return {
        "session_id": session.id,
        "checkout_url": session.url
    }


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()

    try:
        import json
        event = json.loads(payload)
    except Exception as e:
        print("Webhook processing failed:", e)
        raise HTTPException(status_code=400, detail="Invalid webhook")

    print("Webhook received:", event.get("type"))

    if event.get("type") == "checkout.session.completed":
        session = event.get("data", {}).get("object", {})
        user_id = session.get("metadata", {}).get("user_id")
        if not user_id:
            return {"status": "success", "warning": "No user_id in metadata"}

        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid user_id: {user_id}")

        user = db.query(User).filter(User.id == user_uuid).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Avoid duplicate subscriptions
        existing_sub = db.query(Subscription).filter(
            Subscription.stripe_session_id == session.get("id")
        ).first()

        if not existing_sub:
            subscription = Subscription(
                user_id=user.id,
                stripe_session_id=session.get("id"),
                status="active",
                currency=session.get("currency", "INR"),
            )
            db.add(subscription)

        user.is_paid = True
        db.commit()

    return {"status": "success"}


@router.get("/status")
def billing_status(
    current_user: User = Depends(get_current_user),
):
    return {"is_paid": current_user.is_paid}
