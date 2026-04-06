import aiohttp
from disnake import Game
from disnake.ext import tasks

from bot_init import bot, env_cfg, log
from modules.get_round_duration import get_round_duration

timeout = aiohttp.ClientTimeout(total=5)

SS14_RUN_LEVELS = {
    0: "Лобби",
    1: "Раунд",
    2: "Конец"
}


@tasks.loop(seconds=60)
async def monitor_status_ss14():
    log.info("🔍 Проверка статуса сервера SS14...")

    url = f"http://{env_cfg.IP_HOST}:1212/status"

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:

                if resp.status != 200:
                    log.warning(f"⚠️ Код ответа: {resp.status}")
                    return

                data = await resp.json()

                run_level = data.get("run_level", -1)
                round_start = data.get("round_start_time")

                if run_level == 1 and round_start:
                    round_time = get_round_duration(round_start)
                    status_text = f"раунд {round_time}"
                else:
                    status_text = SS14_RUN_LEVELS.get(run_level, "неизвестно")

                players = data.get("players", 0)
                max_players = data.get("soft_max_players", "?")

                log.info(
                    f"✅ {players}/{max_players} | {status_text}"
                )

                await bot.change_presence(
                    activity=Game(
                        name=f"{players}/{max_players} | {status_text}"
                    )
                )

    except Exception as e:
        log.error(f"❌ Ошибка при мониторинге статуса сервера: {e}")
