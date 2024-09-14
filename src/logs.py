import logging
import sys
from src.db.settings import Settings


def setup_logging(settings: Settings) -> None:
    """
    Настройка базового конфигурирования для логирования с использованием переменных окружения.
    """
    log_level = settings.LOG_LEVEL.upper()
    log_file = settings.LOG_FILE
    log_encoding = settings.LOG_ENCODING

    logging.basicConfig(
        level=getattr(logging, log_level, logging.DEBUG),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding=log_encoding),
        ],
    )

    logger = logging.getLogger(__name__)
    logger.debug("Debug level log message")
    logger.info("Info level log message")
    logger.warning("Warning level log message")
    logger.error("Error level log message")
    logger.critical("Critical level log message")
