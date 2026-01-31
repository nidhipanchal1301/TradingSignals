from pydantic import BaseModel

from typing import List



class Signal(BaseModel):
    symbol: str
    action: str
    price: float


class SignalsResponse(BaseModel):
    signals: List[Signal]
