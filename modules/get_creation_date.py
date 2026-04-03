import asyncio
from datetime import datetime

import aiohttp


async def get_creation_date(uuid: str) -> str:
    """
    Получает дату создания аккаунта через API
    """
    url = f"https://auth.spacestation14.com/api/query/userid?userid={uuid}"

    timeout = aiohttp.ClientTimeout(total=5)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:

                if response.status != 200:
                    return f"Ошибка API: {response.status}"

                data = await response.json()

                player_date = data.get("createdTime")
                if not player_date:
                    return "Дата создания не найдена"

                date_obj = datetime.fromisoformat(
                    player_date.replace("Z", "+00:00")
                )

                creation_date_unix = int(date_obj.timestamp())

                return f"<t:{creation_date_unix}:f>"

    except asyncio.TimeoutError:
        return "⏱ Таймаут запроса"

    except aiohttp.ClientError as e:
        return f"Ошибка соединения: {e}"

    except ValueError:
        return "Ошибка при разборе даты"

    except Exception as e:
        return f"Неизвестная ошибка: {e}"
