from app.db.database import engine
from app.models.asset import Base


async def init_database():

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )
