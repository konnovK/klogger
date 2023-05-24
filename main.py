import uvicorn


def main():
    from api.app import app
    from api.globals import settings
    uvicorn.run(app, port=settings.port, host='0.0.0.0')


async def drop():
    from api.globals import db
    from db import metadata
    await db.recreate_all_tables(metadata)
    from api.utils import create_all_log_levels
    await create_all_log_levels()


if __name__ == '__main__':
    main()
    # import asyncio
    # asyncio.run(drop())
