import traceback

from disnake import Client, Embed, TextChannel, User

from bot_init import env_cfg, log


async def log_to_channel(bot: Client, message: str, *,
                         title: str = "Лог",
                         color: int = 0x2f3136,
                         mention: User | None = None,
                         codeblock: bool = True,
                         embed: bool = True,
                         embed_obj: Embed | None = None):
    """
    Универсальная функция логирования в Discord-канал.

    :param bot: Экземпляр бота.
    :param message: Основное сообщение (текст лога).
    :param title: Заголовок эмбеда (если embed=True и embed_obj не передан).
    :param color: Цвет эмбеда (если embed=True и embed_obj не передан).
    :param mention: Упоминание пользователя (если нужно).
    :param codeblock: Обернуть текст в ```, если embed=False.
    :param embed: Использовать embed (по умолчанию True).
    :param embed_obj: Готовый объект Embed, если передан — используется вместо создания нового эмбеда.
    """
    try:
        channel = bot.get_channel(env_cfg.LOG_TECH_CHANNEL)
        if not isinstance(channel, TextChannel):
            log.warning("⚠️ LOG_TECH_CHANNEL не найден или не является текстовым каналом")
            return

        mention_text = f"{mention.mention} " if mention else ""

        if embed:
            if embed_obj is not None:
                # Используем переданный эмбед
                await channel.send(content=mention_text or None, embed=embed_obj)
            else:
                # Создаём эмбед из параметров
                emb = Embed(title=title, description=message, color=color)
                emb.set_footer(text="Логирование")
                await channel.send(content=mention_text or None, embed=emb)
        else:
            if codeblock:
                message = f"```{message}```"
            await channel.send(content=mention_text + message)

        log.info(f"📨 Log sent: {title}")
    except Exception:
        log.error(f"❌ Ошибка при логировании в канал ERROR: {traceback.format_exc()}")
        