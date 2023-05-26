from api.globals import db
from db import metadata
from api.utils import create_all_log_levels
import asyncio


async def drop():
    from api.scheduler import _delete_old_log_items
    await _delete_old_log_items()
    # await db.recreate_all_tables(metadata)
    # await create_all_log_levels()


if __name__ == '__main__':
    asyncio.run(drop())
