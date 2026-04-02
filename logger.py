"""
Модуль логирования для всего приложения.
Использование: from logger import log
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

import pytz

MOSCOW_TIMEZONE = pytz.timezone("Europe/Moscow")


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'


class ColoredFormatter(logging.Formatter):
    """Форматтер с цветами для консоли"""
    
    LEVEL_COLORS = {
        logging.DEBUG: Colors.GRAY,
        logging.INFO: Colors.GREEN,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.BOLD + Colors.RED
    }

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=MOSCOW_TIMEZONE)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def format(self, record):
        levelname = record.levelname
        if sys.stderr.isatty():
            color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)
            record.levelname = f"{color}{levelname}{Colors.RESET}"
        else:
            record.levelname = levelname
            
        return super().format(record)


def setup_logger(name: str = "prismia") -> logging.Logger:
    """
    Создаёт и настраивает логгер с заданным именем.
    
    Args:
        name: Имя логгера (обычно __name__)
        
    Returns:
        Настроенный логгер
    """
    logger = logging.getLogger(name)
    
    # Если логгер уже настроен — возвращаем его
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Формат для логов
    detailed_format = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
    simple_format = '%(asctime)s | %(levelname)-8s | %(message)s'
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColoredFormatter(detailed_format))
    logger.addHandler(console_handler)
    
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler(
            log_dir / "bot.log",
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(ColoredFormatter(detailed_format))
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Не удалось настроить файловое логирование: {e}")
    
    return logger


# Создаём корневой логгер для всего приложения
_logger = setup_logger("chaos")


# Удобные функции для логирования
def debug(msg, *args, **kwargs):
    _logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    _logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    _logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    _logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    _logger.critical(msg, *args, **kwargs)


# Псевдонимы
warn = warning

# Для обратной совместимости
log_setup = _logger

__all__ = [
    'log', 'debug', 'info', 'warning', 'warn', 
    'error', 'critical', 'setup_logger'
]
