"""
Этот модуль инициализирует бота для работы с Discord.
Настроены необходимые параметры для запуска и обработки команд.
"""

import disnake
from disnake.ext import commands

from config import ENVIRONMENT_VAR
from logger import log_setup
from modules.database_manager import DatabasePostgreSQLManagerSS14

# Менеджер для доступа к переменным окружения
env_cfg = ENVIRONMENT_VAR()

# Инициализация бота с необходимыми интентами и параметрами
intents = disnake.Intents.all()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.guilds = True
bot = commands.Bot(
    command_prefix=env_cfg.COMMANDS_PREFIX,
    help_command=None,
    intents=intents,
    test_guilds=[1424305560966140004],
    sync_commands=True,
)

# Инициализация логгера
log = log_setup

# Инициализация менеджера БД
ss14_db = DatabasePostgreSQLManagerSS14()
