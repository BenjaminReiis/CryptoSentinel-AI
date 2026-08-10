import asyncio
import json
from datetime import datetime, timezone

import websockets

from app.core.config import settings
from app.db.database import AsyncSessionLocal
from app.models.market import MarketPrice


SYMBOLS = [
    "btcusdt",
    "ethusdt",
    "solusdt",
]


def normalize_symbol(symbol: str) -> str:
    return symbol.upper()


async def save_market_price(
    symbol: str,
    price: float,
    quantity: float | None,
    event_time: int,
):
    async with AsyncSessionLocal() as session:

        market_price = MarketPrice(
            symbol=normalize_symbol(symbol),
            price=price,
            quantity=quantity,
            event_time=datetime.fromtimestamp(
                event_time / 1000,
                tz=timezone.utc,
            ).replace(tzinfo=None),
        )

        session.add(market_price)

        await session.commit()


async def market_stream():
    streams = "/".join(
        f"{symbol}@trade"
        for symbol in SYMBOLS
    )

    url = (
        "wss://stream.binance.com:9443/stream"
        f"?streams={streams}"
    )

    print("Conectando ao mercado...")
    print(url)

    async with websockets.connect(url) as websocket:

        print("Market stream conectado.")

        async for message in websocket:

            data = json.loads(message)

            trade = data.get("data")

            if not trade:
                continue

            symbol = trade["s"]

            price = float(trade["p"])

            quantity = float(trade["q"])

            event_time = int(trade["T"])

            print(
                f"{symbol} | "
                f"${price:,.4f} | "
                f"qty={quantity}"
            )

            await save_market_price(
                symbol=symbol,
                price=price,
                quantity=quantity,
                event_time=event_time,
            )


async def start_market_collector():

    while True:

        try:

            await market_stream()

        except Exception as error:

            print(
                f"Erro no market stream: {error}"
            )

            print(
                "Reconectando em 5 segundos..."
            )

            await asyncio.sleep(5)
