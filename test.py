import random
import uuid
from loguru import logger
from clients.klogger import KLoggerHandler

handler = KLoggerHandler('185.221.213.55:8080', 'konnovki@yandex.ru', '123', '3a9e46a0-3568-454b-a5ba-c825eeeca219')

logger.add(handler, enqueue=True, level='DEBUG')

i = 1
while True:
    log_level = random.choice(['DEBUG', 'DEBUG', 'INFO', 'INFO', 'WARNING', 'ERROR'])
    log_message = f'Second test obj {i}: {uuid.uuid4()}'
    logger.log(log_level, log_message)
    i += 1
