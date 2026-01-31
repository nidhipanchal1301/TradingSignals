#!/bin/bash

echo "Deploying TradingSignals..."

pip install --upgrade pip
pip install -r requirements.txt

alembic upgrade head

uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
