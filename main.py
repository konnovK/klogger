import asyncio
from loguru import logger

logger.add('.log/.log', level='DEBUG', rotation='10 MB', compression="gz")

from api.app import app
from api.scheduler import scheduler
from api.globals import settings, db, telegram_bot
import uvicorn


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""
    def handle_exit(self, sig: int, frame) -> None:
        logger.info(f"STOP SERVER ON port={settings.port}")
        scheduler.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    from db.schema import metadata
    await db.create_all_tables(metadata)

    if telegram_bot is not None:
        logger.info(f'START TELEGRAM BOT')
        await telegram_bot.initialize()

    "Run scheduler and the API"
    server = Server(config=uvicorn.Config(app, host='0.0.0.0', port=settings.port, access_log=False))

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(scheduler.serve())

    await asyncio.wait([sched, api])

    if telegram_bot is not None:
        logger.info(f'STOP TELEGRAM BOT')
        await telegram_bot.shutdown()

if __name__ == "__main__":
    logger.info(f"START SERVER ON port={settings.port}")
    asyncio.run(main())
