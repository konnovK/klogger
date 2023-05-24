from loguru import logger
from klogger import KLoggerHandler

handler = KLoggerHandler('http://localhost:8080', 'user@example.com', 'string', '4f62934f-5f07-4246-97ed-049926bd72db')

logger.add(handler)


for i in range(10000):
    logger.info(f'test {i}')
