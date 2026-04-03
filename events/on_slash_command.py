from disnake import AppCommandInteraction, Embed

from bot_init import bot
from modules.send_log_to_channel import log_to_channel


@bot.event
async def on_slash_command(interaction: AppCommandInteraction, result=None):
    """
    Логирует выполнение слэш-команды в указанный канал
    
    :param interaction: Объект взаимодействия команды
    :param result: Результат выполнения команды (опционально)
    """
    try:
        message = await interaction.original_message()
        message_url = f"https://discord.com/channels/{interaction.guild_id}/{interaction.channel_id}/{message.id}"
    except Exception:
        message_url = f"https://discord.com/channels/{interaction.guild_id}/{interaction.channel_id}"

    user = interaction.user
    guild = interaction.guild
    command_name = interaction.application_command.name
    options = interaction.data.get("options", [])

    # Форматируем аргументы команды
    args_str = ", ".join(
        f"{opt['name']}={opt['value']}" 
        for opt in options
        if isinstance(opt, dict) and 'name' in opt and 'value' in opt
    ) or "без аргументов"

    embed = Embed(
        title=f"Команда: /{command_name}",
        color=0x2f3136,
        timestamp=interaction.created_at,
    )
    
    embed.description = (
        f"👤 {user} (`{user.id}`)\n"
        f"📁 {guild.name if guild else 'DM'} / "
        f"{getattr(interaction.channel, 'name', 'N/A')}\n"
        f"📝 Аргументы: {args_str}\n"
        f"[Перейти к сообщению]({message_url})"
    )

    # Добавляем информацию о результате, если он есть
    if result is not None:
        embed.add_field(name="Результат", value=str(result)[:1000], inline=False)

    # Отправляем лог
    await log_to_channel(
        bot=interaction.bot,
        message="",
        embed_obj=embed,
        title="slash_command"
    )
    