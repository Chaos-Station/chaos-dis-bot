import asyncio

import aiohttp
from disnake import AppCommandInteraction
from disnake.ext import commands

from bot_init import bot, env_cfg
from modules.check_roles import has_any_role_by_keys


async def send_instance_request(action: str):
    url = f"http://{env_cfg.IP_HOST}:5000/instances/{env_cfg.NAME_INST}/{action}"

    auth = aiohttp.BasicAuth(env_cfg.NAME_INST, env_cfg.POST_REQUEST_WATCHDOG)

    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, auth=auth) as response:
            text = await response.text()
            return response.status, text


async def handle_request(inter, action: str):
    try:
        status, text = await send_instance_request(action)

        if status == 200:
            msg = f"✅ Запрос `{action}` отправлен."
        else:
            msg = (
                f"⚠️ Сервер вернул ошибку.\n"
                f"Status: **{status}**\n"
                f"```{text}```"
            )

    except asyncio.TimeoutError:
        msg = "⏱ Сервер не ответил (timeout 10s)."

    except aiohttp.ClientError as e:
        msg = f"❌ Ошибка запроса:\n```{e}```"

    return msg


# ---------------- SLASH COMMANDS ----------------

@bot.slash_command(
    name="restart",
    description="Посылает запрос на рестарт сервера.",
    guild_ids=[env_cfg.GUILD_DISCORD_SERVER_ID]
)
@has_any_role_by_keys("head_team")
async def restart_command(inter: AppCommandInteraction):

    await inter.response.defer(ephemeral=True)
    msg = await handle_request(inter, "restart")
    await inter.edit_original_response(msg)


@bot.slash_command(
    name="update",
    description="Посылает запрос на обновление сервера.",
    guild_ids=[env_cfg.GUILD_DISCORD_SERVER_ID]
)
@has_any_role_by_keys("head_team")
async def update_command(inter: AppCommandInteraction):

    await inter.response.defer(ephemeral=True)
    msg = await handle_request(inter, "update")
    await inter.edit_original_response(msg)


# ---------------- TEXT COMMANDS ----------------

@bot.command(name="restart")
@has_any_role_by_keys("head_team")
async def restart_text(ctx: commands.Context):

    msg = await handle_request(ctx, "restart")
    await ctx.send(msg)


@bot.command(name="update")
@has_any_role_by_keys("head_team")
async def update_text(ctx: commands.Context):

    msg = await handle_request(ctx, "update")
    await ctx.send(msg)
    