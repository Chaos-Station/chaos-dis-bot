import time
from collections import defaultdict

import disnake
from disnake import Option
from disnake.ext import commands

from bot_init import bot, env_cfg, log, ss14_db
from data import delete_user_data, get_user_by_code, get_user_data
from modules.check_roles import has_any_role_by_keys
from modules.get_creation_date import get_creation_date

# Словарь для отслеживания времени последнего использования команды
# Структура: { (channel_id, user_id): last_used_timestamp }
user_cooldown = defaultdict(float)

# Настройки
USER_COOLDOWN_SECONDS = env_cfg.DISCORD_AUTH_USER_COOLDOWN_SECONDS  # 60 минут между использованием у одного пользователя
ALLOWED_CHANNEL_ID = env_cfg.DISCORD_AUTH_CHANNEL_ID  # ЗАМЕНИТЬ НА ID СВОЕГО КАНАЛА


@bot.command(
    name="link",
    description="Привязать аккаунт по коду. Доступно только в специальном канале."
)
async def link_account(ctx, code: str):
    """
    Команда доступна всем пользователям в специальном канале.
    Привязывает Discord ID к userId по коду.
    """
    tech_channel = bot.get_channel(env_cfg.LOG_TECH_CHANNEL)
    
    # Проверка канала
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        log.warning(f"❌ {ctx.author} попытался использовать команду не в том канале: {ctx.channel.name}")
        # Можно ничего не отвечать или ответить и удалить
        await ctx.send(f"⛔ Эту команду можно использовать только в канале <#{ALLOWED_CHANNEL_ID}>.", delete_after=10)
        return
    
    # Проверка на спам (cooldown для каждого пользователя)
    current_time = time.time()
    cooldown_key = (ctx.channel.id, ctx.author.id)
    last_used = user_cooldown[cooldown_key]
    
    if current_time - last_used < USER_COOLDOWN_SECONDS:
        remaining = int(USER_COOLDOWN_SECONDS - (current_time - last_used))
        await ctx.send(
            f"⏳ {ctx.author.mention}, подождите {remaining} сек. перед следующим использованием.",
            delete_after=remaining
        )
        return
    
    # Обновляем время последнего использования
    user_cooldown[cooldown_key] = current_time
    
    # Поиск данных по коду в памяти
    log.info(f"🔍 {ctx.author} ввёл код: {code}")
    
    user_data = None
    found_user_id = None
    
    # Проходим по всем данным в памяти
    found_user_id = get_user_by_code(code)

    if not found_user_id:
        log.warning(f"⚠️ Код {code} не найден (пользователь {ctx.author})")
        await ctx.send(
            f"❌ {ctx.author.mention}, код `{code}` не найден. Проверьте правильность ввода.",
            delete_after=15
        )
        return    
    
    discord_id = ctx.author.id
    user_id = found_user_id


    if ss14_db.is_user_linked(user_id, discord_id):
        log.warn(f"⚠️ Пользователь {ctx.author} уже привязан к userId {user_id}")
        await tech_channel.send(
            f"⚠️ Пользователь {ctx.author} уже привязан к userId {user_id} (код: {code})"
        )
        return

    player_data = ss14_db.fetch_player_data_by_user_id(user_id)
    if not player_data:
        await tech_channel.send(
            f"⚠️ Не найден игрок с userId {user_id} для Discord {ctx.author} (код: {code})"
        )
        return
    
    creation_date = await get_creation_date(user_id)

    ss14_db.link_user_to_discord(user_id, discord_id)

    user = await bot.fetch_user(discord_id)
    userNamePlayer = ss14_db.get_username_by_user_id(user_id)
    log.info(f"✅ Успешная привязка: Discord {user.name} -> userId {user_id} (игрок: {userNamePlayer}, создан: {creation_date})")
    await tech_channel.send(
        f"✅ Успешная привязка: Discord {user.name} -> userId {user_id} (игрок: {userNamePlayer}, создан: {creation_date})"
    )
    
    # Удаляем данные из памяти после успешной привязки
    delete_user_data(user_id)
    log.info(f"🗑️ Данные для userId {user_id} удалены из памяти")
    
    # Отправляем подтверждение пользователю
    await ctx.send(
        f"✅ {ctx.author.mention}, ваш аккаунт успешно привязан!"
    )
    
    # Выдать роль
    bot_guild = bot.get_guild(env_cfg.GUILD_DISCORD_SERVER_ID)
    role = bot_guild.get_role(env_cfg.DISCORD_VERIFED_ROLE_ID)
    if role:
        await ctx.author.add_roles(role, reason="Привязка аккаунта")
        log.info(f"🎖️ Роль успешно выдана пользователю {ctx.author}")
    else:
        log.error(f"❌ Роль с ID {env_cfg.DISCORD_VERIFED_ROLE_ID} не найдена на сервере {bot_guild.name}")

@bot.slash_command(name="dis_link", description="(АДМИН) Привязывает игрового пользователя к Discord.", guild_ids=[env_cfg.GUILD_DISCORD_SERVER_ID])
@has_any_role_by_keys("head_team")
async def link_dis(
    inter: disnake.ApplicationCommandInteraction,
    nickname: str = Option(
            name="nickname",
            description="Никнейм в игре",
            required=True
            ),
    discord: disnake.Member = Option(
                name="discord",
                description="Пинг или имя в Discord",
                required=True
            )
):
    """
    Привязывает игрового пользователя к Discord.
    
    Использование: /linc_dis <ник в игре> <пинг или имя в Discord>
    """

    # Получаем данные игрока из базы
    player_data = ss14_db.fetch_player_data(nickname)

    if not player_data:
        await inter.response.send_message(f"❌ Игрок с ником `{nickname}` не найден в базе данных.")
        return

    player_id, user_id, *_ = player_data
    discord_id = discord.id

    # Проверяем, не привязан ли уже этот
    # пользователь или дискорд-аккаунт
    if ss14_db.is_user_linked(user_id, discord_id):
        await inter.response.send_message(
            "⚠️ Этот Discord-аккаунт или "
            "игровой профиль уже привязан."
        )
        return

    # Привязываем пользователя
    ss14_db.link_user_to_discord(user_id, discord_id)
    # ss14_db.link_user_to_discord(user_id, discord_id, "dev")

    await inter.response.send_message(
        f"✅ Игровой профиль `{nickname}` успешно "
        f"привязан к {discord.mention}."
    )


@bot.slash_command(name="dis_unlink", description="(АДМИН) Удаляет привязку Discord-аккаунта.", guild_ids=[env_cfg.GUILD_DISCORD_SERVER_ID])
@has_any_role_by_keys("head_team")
async def unlink_dis(
    inter: disnake.ApplicationCommandInteraction,
    discord: disnake.Member = Option(name="discord", description="Пинг Discord", required=True)
):
    """
    Удаляет привязку Discord-аккаунта.
    """

    result = ss14_db.unlink_user_from_discord(discord)
    # result_dev = ss14_db.unlink_user_from_discord(discord, "dev")

    message = ""

    if result:
        message += f"✅ Привязка для {discord.mention} удалена.\n"
    else:
        message += f"❌ Привязка для {discord.mention} не найдена.\n"

    await inter.response.send_message(message)

@link_account.error
async def link_account_error(ctx, error):
    """Обработчик ошибок"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ {ctx.author.mention}, укажите код. Пример: `!link ABC123`", delete_after=15)
    else:
        log.error(f"Ошибка в команде link: {error}")
        await ctx.send("❌ Произошла ошибка при выполнении команды.", delete_after=10)



