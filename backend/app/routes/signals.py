from fastapi import APIRouter, Depends

from ..dependencies import get_current_user

from ..services.signal_service import fetch_signals



router = APIRouter()

@router.get("/signals")
def get_signals(current_user = Depends(get_current_user), paid: bool = False):
    return fetch_signals(paid=paid)
