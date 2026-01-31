from ..crud.signal import get_signals
import json
import fakeredis



redis_client = fakeredis.FakeStrictRedis()

CACHE_KEY = "signals_cache"

def fetch_signals(paid: bool):
    cached = redis_client.get(f"{CACHE_KEY}_{paid}")
    if cached:
        return json.loads(cached)

    signals = [s.dict() for s in get_signals(paid=paid)]

    redis_client.set(f"{CACHE_KEY}_{paid}", json.dumps(signals), ex=300)
    return signals
