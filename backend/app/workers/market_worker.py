import asyncio

from app.services.market_collector import (
    start_market_collector,
)


if __name__ == "__main__":

    asyncio.run(
        start_market_collector()
    )
