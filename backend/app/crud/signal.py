from typing import List

from ..schemas.signal import Signal



MOCK_SIGNALS = [
    {"symbol": "NIFTY", "action": "BUY", "price": 17500, "is_premium": True},
    {"symbol": "BANKNIFTY", "action": "SELL", "price": 42000, "is_premium": True},
    {"symbol": "RELIANCE", "action": "BUY", "price": 2500, "is_premium": False},  # free signal
]

def get_signals(paid: bool = False) -> List[Signal]:

    if paid:
        return [Signal(**s) for s in MOCK_SIGNALS]
    else:
        return [Signal(**s) for s in MOCK_SIGNALS if not s.get("is_premium", True)]
