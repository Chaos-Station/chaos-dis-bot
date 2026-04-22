from disnake.ext import tasks

from bot_init import bot, env_cfg, ss14_db, log


@tasks.loop(hours=12)
async def check_size_log():
    try:
        log.info("🔍 Проверка размера логов БД SS14...")
        log_channel = bot.get_channel(env_cfg.LOG_TECH_CHANNEL)
        if not log_channel:
            print("❌ Не удалось получить канал логов.")
            await log_channel.send("❌ Не удалось получить канал логов.")
            return

        for db_name in ['main']:
            tables, _ = ss14_db.get_tables_size(db_name)

            for table in tables:
                if table["table"] == "admin_log":
                    size_str = table["size"]
                    size_parts = size_str.split()

                    if len(size_parts) != 2:
                        print(f"⚠️ Невалидный размер таблицы admin_log в {db_name}: {size_str}")
                        continue

                    size_value, size_unit = size_parts
                    size_value = float(size_value.replace(',', '.'))

                    # Приводим размер к гигабайтам
                    if size_unit.upper() in ['MB', 'МБ']:
                        size_in_gb = size_value / 1024
                    elif size_unit.upper() in ['GB', 'ГБ']:
                        size_in_gb = size_value
                    else:
                        print(f"⚠️ Неизвестная единица размера: {size_unit}")
                        continue

                    if size_in_gb > 17:
                        await log_channel.send(
                            f"🚨 **Предупреждение!** Таблица `admin_log` в базе данных `{db_name}` "
                            f"превысила 17 ГБ! 📊\n"
                            f"Текущий размер: **{size_str}**\n"
                            f"Размер в гигабайтах: **{size_in_gb:.2f} GB**\n"
                            f"⚠️ Требуется внимание! <@&1489256771167060038>"
                        )
                    else:
                        await log_channel.send(
                            f"ℹ️ Размер admin_log в `{db_name}`: {size_in_gb:.2f} GB (порог 17 GB)"
                        )
    except Exception as e:
        msg = f"Ошибка в check_size_log: {e}"
        print(msg)
        await log_channel.send(f"❌ {msg}")


# TODO: Доделать чтобы при превышении 17 Гб, 
# прописывались эти скрипты
"""sql
DELETE FROM admin_log
WHERE round_id NOT IN (
    SELECT DISTINCT round_id 
    FROM admin_log 
    ORDER BY round_id DESC 
    LIMIT 70
);

VACUUM FULL ANALYZE admin_log;


DELETE FROM admin_log_player
WHERE round_id NOT IN (
    SELECT DISTINCT round_id FROM admin_log
);

VACUUM FULL ANALYZE admin_log_player;
"""