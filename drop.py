from api.globals import db
from db import metadata
from api.utils import create_all_log_levels
import asyncio


async def drop():
    await db.recreate_all_tables(metadata)
    await create_all_log_levels()


if __name__ == '__main__':
    asyncio.run(drop())
