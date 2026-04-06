"""
Этот модуль содержит все основные конфигурации chaos-bot.
"""

import os

import pytz
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

def get_env_variable(name: str, default: str = None) -> str:
    """
    Получает переменную окружения. Если не найдена и default=None - вызывает ошибку.
    """
    value = os.getenv(name)
    if value is None:
        if default is None:
            print(f"КРИТИЧЕСКАЯ ОШИБКА: Переменная {name} обязательна!")
            raise ValueError(f"Не найдена обязательная переменная: {name}")
        print(f"Предупреждение: {name} не найден. Используется default: {default}")
        return default
    return value


class ENVIRONMENT_VAR:
    """Класс для доступа к переменным окружения"""
    _instance = None

    MOSCOW_TIMEZONE = pytz.timezone("Europe/Moscow")
    DISCORD_VERIFED_ROLE_ID = 1489259411850661918
    MY_USER_ID = 328502766622474240
    IP_HOST = "80.66.85.166"
    NAME_INST = "chaos-station-inst"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def DISCORD_TOKEN(self) -> str:
        """Токен Discord бота (обязательный)"""
        return get_env_variable("DISCORD_TOKEN", "NULL")
    
    @property
    def REPO_NAME(self) -> str:
        """Название репозитория (по умолчанию 'chaos-bot')"""
        return get_env_variable("REPO_NAME", "chaos-dis-bot")
    
    @property
    def AUTHOR_NAME(self) -> str:
        """Имя автора (по умолчанию 'Chaos-Station')"""
        return get_env_variable("AUTHOR_NAME", "Chaos-Station")
    
    @property
    def LOG_TECH_CHANNEL(self) -> int:
        """ID канала для логов (по умолчанию 1374529148474622085)"""
        return int(get_env_variable("LOG_TECH_CHANNEL", "1489251952658481284"))
    
    @property
    def GUILD_DISCORD_SERVER_ID(self) -> int: 
        """ID Discord сервера (по умолчанию 1475918847759356117)"""
        return int(get_env_variable("GUILD_DISCORD_SERVER_ID", "1424305560966140004"))
    
    @property
    def COMMANDS_PREFIX(self) -> str:
        """Префикс для команд бота (по умолчанию '$')"""
        return get_env_variable("COMMANDS_PREFIX", "$")
    
    @property
    def HTTP_SERVER_PORT(self) -> int:
        """Порт для HTTP сервера (по умолчанию 9010)"""
        return int(get_env_variable("HTTP_SERVER_PORT", "9010"))
    
    @property
    def HTTP_SERVER_TOKEN(self) -> str:
        """Токен для авторизации на HTTP сервере (по умолчанию 'my_secret_token_123')"""
        return get_env_variable("HTTP_SERVER_TOKEN", "my_secret_token_123")
    
    @property
    def DISCORD_AUTH_USER_COOLDOWN_SECONDS(self) -> int:
        """Cooldown для команд, связанных с привязкой аккаунта (по умолчанию 3600 секунд)"""
        return int(get_env_variable("DISCORD_AUTH_USER_COOLDOWN_SECONDS", "3600"))
    
    @property
    def DISCORD_AUTH_CHANNEL_ID(self) -> int:
        """ID канала для команд привязки аккаунта (по умолчанию 1481280582368493761)"""
        return int(get_env_variable("DISCORD_AUTH_CHANNEL_ID", "1490642843067355226"))

    @property
    def POSTGRES_DATABASE(self) -> str:
        """Название базы данных PostgreSQL (по умолчанию 'ss14_prod')"""
        return get_env_variable("POSTGRES_DATABASE", "ss14_prod")
    
    @property
    def POSTGRES_USER(self) -> str:
        """Пользователь для подключения к PostgreSQL (по умолчанию 'postgres')"""
        return get_env_variable("POSTGRES_USER", "postgres")
    
    @property
    def POSTGRES_PASSWORD(self) -> str:
        """Пароль для подключения к PostgreSQL (по умолчанию 'password')"""
        return get_env_variable("POSTGRES_PASSWORD", "password")
    
    @property
    def POSTGRES_HOST(self) -> str:
        """Хост для подключения к PostgreSQL (по умолчанию 'localhost')"""
        return get_env_variable("POSTGRES_HOST", "localhost")
    
    @property
    def POSTGRES_PORT(self) -> int:
        """Порт для подключения к PostgreSQL (по умолчанию 5432)"""
        return int(get_env_variable("POSTGRES_PORT", "5432"))
    
    @property
    def POST_REQUEST_WATCHDOG(self) -> str:
        return get_env_variable("POST_REQUEST_WATCHDOG", "NULL")
    

    ROLE_WHITELISTS = {
        # Ключи ID ролей для вайтлистов
        # "whitelist_role_id": [
        #     1060191651538145420,  # Разработка
        #     1347877224430436493,  # Глава проекта
        #     1060264704838209586,  # Куратор Проекта
        #     1054908932868538449,  # Руководитель проекта
        #     1054827766211694593,  # Админ
        #     1127152229439246468,  # Зам. создателя проекта
        #     1266161300036390913,  # Руководство отдела разработки
        # ],
        "head_team": [
            1424305770274754660,  # Глава проекта
        ],
    }

# # Инициализация класса
# env_cfg = ENVIRONMENT_VAR()
# """Класс для доступа к переменным окружения в стиле ENVIRONMENT_VAR.KEY"""
