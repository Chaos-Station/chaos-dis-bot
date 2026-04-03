import aiohttp
from disnake import Embed

from bot_init import bot, env_cfg
from modules.get_round_duration import get_round_duration

timeout = aiohttp.ClientTimeout(total=5)

SS14_RUN_LEVELS = {
    0: "🕓 Лобби",
    1: "🟢 Раунд идёт",
    2: "🔴 Окончание раунда"
}


@bot.command(name="status")
async def status_command(ctx, server: str = "mrp"):
    """Команда для получения информации о сервере"""

    if server.lower() == "mrp":
        address = env_cfg.IP_HOST
        port = "1212"

    url = f"http://{address}:{port}/status"

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:

                if resp.status != 200:
                    await ctx.send(f"Ошибка: код {resp.status}")
                    return

                data = await resp.json()

                run_level = data.get("run_level", -1)
                round_start = data.get("round_start_time")

                if run_level == 1 and round_start:
                    round_time = get_round_duration(round_start)
                else:
                    round_time = SS14_RUN_LEVELS.get(run_level, "❓ Неизвестно")

                embed = Embed(
                    title="Статус сервера",
                    color=0x8b0000
                )

                embed.add_field(
                    name="Название",
                    value=data.get("name", "Неизвестно"),
                    inline=False
                )

                embed.add_field(
                    name="Игроки",
                    value=f"{data.get('players', 0)}/{data.get('soft_max_players', '?')}",
                    inline=False
                )

                embed.add_field(
                    name="Время раунда",
                    value=round_time,
                    inline=False
                )

                embed.add_field(
                    name="Раунд ID",
                    value=data.get("round_id", "N/A"),
                    inline=False
                )

                await ctx.send(embed=embed)

    except Exception as e:
        import traceback
        traceback.print_exc()
        await ctx.send(f"Ошибка: {e}")
