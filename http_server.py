"""
Простой HTTP-сервер для приёма JSON-запросов.
Проверяет токен и сохраняет данные в memory_storage.
"""

import json

from aiohttp import web

from bot_init import env_cfg, log
from data import save_user_data

logger = log.getChild("http_server")
VALID_TOKEN = env_cfg.HTTP_SERVER_TOKEN

async def handle_post(request):
    """Обрабатывает POST-запросы с JSON"""
    try:
        # Получаем JSON из тела запроса
        data = await request.json()
        logger.info(f"📥 Получен запрос: {data}")
        
        # Проверяем наличие всех полей
        if not all(k in data for k in ("userId", "code", "token")):
            return web.json_response({
                "status": "error",
                "message": "Missing required fields: userId, code, token"
            }, status=400)
        
        # Проверяем токен
        if data["token"] != VALID_TOKEN:
            logger.warning(f"⚠️ Неверный токен от userId: {data['userId']}")
            return web.json_response({
                "status": "error",
                "message": "Invalid token"
            }, status=403)
        
        # Сохраняем данные
        success = save_user_data(
            userId=data["userId"],
            code=data["code"],
            token=data["token"]
        )
        
        if success:
            return web.json_response({
                "status": "ok",
                "message": "Data saved"
            })
        else:
            return web.json_response({
                "status": "error",
                "message": "Failed to save data"
            }, status=500)
            
    except json.JSONDecodeError:
        logger.error("❌ Неверный JSON")
        return web.json_response({
            "status": "error",
            "message": "Invalid JSON"
        }, status=400)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return web.json_response({
            "status": "error",
            "message": str(e)
        }, status=500)

async def init_http_server():
    """Инициализация HTTP-сервера"""
    app = web.Application()
    app.router.add_post('/auth', handle_post)
    return app
