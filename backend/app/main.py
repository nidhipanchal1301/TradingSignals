from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import user, subscription

from .database.db import engine, Base

from .routes import auth, billing, signals



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trading Signals SaaS")

origins = [
    "http://localhost:3000",
    "https://trading-signals-production.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(billing.router)
app.include_router(signals.router)
