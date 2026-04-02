import json
import os

from bot_init import log

DATA_FILE = os.path.join("data", "storage.json")

memory_storage = {}
code_index = {}


def load_data():
    global memory_storage, code_index

    if not os.path.exists(DATA_FILE):
        log.warning("⚠️ storage.json не найден, создаём новый")
        save_data()
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            memory_storage = json.load(f)

        # восстанавливаем индекс
        code_index = {
            str(v["code"]): userId
            for userId, v in memory_storage.items()
        }

        log.info("✅ Данные загружены из JSON")

    except Exception as e:
        log.error(f"❌ Ошибка загрузки JSON: {e}")


def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(memory_storage, f, indent=4, ensure_ascii=False)

    except Exception as e:
        log.error(f"❌ Ошибка сохранения JSON: {e}")


def save_user_data(userId: str, code: str, token: str) -> bool:
    try:
        code = str(code)

        if userId in memory_storage:
            old_code = memory_storage[userId]["code"]

            if str(old_code) in code_index:
                del code_index[str(old_code)]

        if code in code_index:
            old_user = code_index[code]
            log.warning(f"⚠️ Код {code} уже был у {old_user}")

        memory_storage[userId] = {
            "code": code,
            "token": token
        }

        code_index[code] = userId

        save_data()

        return True

    except Exception as e:
        log.error(f"❌ Ошибка: {e}")
        return False


def get_user_by_code(code: str):
    return code_index.get(str(code))


def get_user_data(userId: str):
    return memory_storage.get(userId)


def delete_user_data(userId: str):
    if userId in memory_storage:
        code = memory_storage[userId]["code"]

        del memory_storage[userId]

        if str(code) in code_index:
            del code_index[str(code)]

        save_data()

        return True

    return False
