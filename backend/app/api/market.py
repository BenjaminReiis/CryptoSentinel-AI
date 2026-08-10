from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.market import MarketPrice


router = APIRouter(
    prefix="/api/v1/market",
    tags=["Market"],
)


@router.get("")
async def get_market(
    db: AsyncSession = Depends(get_db),
):

    query = (
        select(MarketPrice)
        .order_by(desc(MarketPrice.event_time))
        .limit(50)
    )

    result = await db.execute(query)

    prices = result.scalars().all()

    return [
        {
            "symbol": item.symbol,
            "price": item.price,
            "quantity": item.quantity,
            "event_time": item.event_time,
        }
        for item in prices
    ]


@router.get("/{symbol}")
async def get_symbol_market(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):

    symbol = symbol.upper()

    query = (
        select(MarketPrice)
        .where(
            MarketPrice.symbol == symbol
        )
        .order_by(
            desc(MarketPrice.event_time)
        )
        .limit(100)
    )

    result = await db.execute(query)

    prices = result.scalars().all()

    if not prices:

        raise HTTPException(
            status_code=404,
            detail="Ativo ainda não encontrado.",
        )

    return [
        {
            "symbol": item.symbol,
            "price": item.price,
            "quantity": item.quantity,
            "event_time": item.event_time,
        }
        for item in prices
    ]
