from sqlalchemy.orm import Session

from ..models.subscription import Subscription

from uuid import UUID



def create_subscription(db: Session, user_id: UUID, stripe_session_id: str, currency: str = "INR") -> Subscription:
    sub = Subscription(user_id=user_id, stripe_session_id=stripe_session_id, currency=currency)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


def get_subscription_by_session(db: Session, session_id: str):
    return db.query(Subscription).filter(Subscription.stripe_session_id == session_id).first()


def mark_subscription_completed(db: Session, session_id: str):
    sub = get_subscription_by_session(db, session_id)
    if sub:
        sub.status = "completed"
        db.commit()
        db.refresh(sub)
    return sub
