"""
Модуль для запуска приложения.
"""
import asyncio
import importlib
import pkgutil
from pathlib import Path

from aiohttp import web

from bot_init import bot, env_cfg, log
from data import load_data
from http_server import init_http_server


def load_modules(folder: str):
    package = importlib.import_module(folder)
    if not package.__file__:
        return
    dir_path = Path(package.__file__).parent
    for _, mod_name, _ in pkgutil.iter_modules([str(dir_path)]):
        importlib.import_module(f"{folder}.{mod_name}")


async def run_http_server():
    """Запуск HTTP-сервера"""
    app = await init_http_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', env_cfg.HTTP_SERVER_PORT)
    await site.start()
    log.info(f"🌐 HTTP-сервер запущен на порту {env_cfg.HTTP_SERVER_PORT}")
    return runner


async def main():
    load_data() # Инициализация данных из JSON при запуске
    # Автоматический импорт всех модулей
    load_modules('commands.admin')
    load_modules('commands.discord')
    # load_modules('commands.misc')
    load_modules("events")
    load_modules("tasks")
    load_modules("modules")
    # . . .

    http_runner = await run_http_server()
    
    if env_cfg.DISCORD_TOKEN == "NULL":
        log.error("КРИТИЧЕСКАЯ ОШИБКА: DISCORD_TOKEN не найден!")
        return
    else:
        log.info("Запуск бота...")
        try:
            await bot.start(env_cfg.DISCORD_TOKEN)
        finally:
            await http_runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
