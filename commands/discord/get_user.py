from disnake import Member

from bot_init import bot, ss14_db
from modules.check_roles import has_any_role_by_keys


@bot.command()
@has_any_role_by_keys("whitelist_role_id_administration_post", "general_adminisration_role")
async def get_ckey(ctx, discordUser: Member):
    """Получить ckey (ник в SS14) пользователя по его Discord."""
    try:
        user_id = ss14_db.get_user_id_by_discord_id(str(discordUser.id))
        if not user_id:
            await ctx.send(f"❌ Пользователь {discordUser.mention} не привязан к SS14!")
            return

        userName = ss14_db.get_username_by_user_id(user_id)
        if not userName:
            await ctx.send(f"⚠ Никнейм не найден в базе данных.")
            return

        await ctx.send(
            f"🔹 **Discord:** {discordUser.name} (ID: {discordUser.id})\n"
            f"🔹 **SS14 ник:** `{userName}`"
        )
    except Exception as e:
        await ctx.send(f"🚫 Ошибка при получении данных: `{str(e)}`")
        raise

@bot.command()
@has_any_role_by_keys("whitelist_role_id_administration_post", "general_adminisration_role")
async def get_discord(ctx, ckey: str):
    """Получить Discord пользователя по его ckey (нику в SS14)."""
    try:
        user_id = ss14_db.get_user_id_by_username(ckey)
        if not user_id:
            await ctx.send(f"❌ Пользователь с ником `{ckey}` не найден в базе данных!")
            return

        discord_id = ss14_db.get_discord_id_by_user_id(user_id)
        if not discord_id:
            await ctx.send(f"⚠ Discord-аккаунт не найден для пользователя `{ckey}`.")
            return
        
        discordMember = bot.get_user(int(discord_id))
        await ctx.send(
            f"🔹 **SS14 ник:** `{ckey}`\n"
            f"🔹 **Discord ID:** {discordMember.name} (ID: {discordMember.id})"
        )
    except Exception as e:
        await ctx.send(f"🚫 Ошибка при получении данных: `{str(e)}`")
        raise
    