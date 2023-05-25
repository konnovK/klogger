from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine


class DB:
    engine: AsyncEngine
    async_session: async_sessionmaker[AsyncSession]

    def __init__(
            self, 
            db_user: str,
            db_password: str,
            db_host: str,
            db_port: str,
            db_name: str,
            debug: bool = False
    ) -> None:
        logger.info(f"INITIALIZE DB WITH {debug=}")
        postgres_dsn = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        self.engine = create_async_engine(
            postgres_dsn,
            echo=debug,
            pool_size=20,
            max_overflow=40,
        )
        self.async_session = async_sessionmaker(self.engine)
    
    async def recreate_all_tables(self, metadata):
        logger.info("RECREATE ALL TABLES")
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)
