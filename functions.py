import aiohttp
import uuid
import json
import logging
from datetime import datetime, timedelta
from config import XUI_API_URL, XUI_USERNAME, XUI_PASSWORD
from database import StaticProfileHelper, UserHelper  

logger = logging.getLogger(__name__)

async def create_profile_for_user(telegram_id: int, tx_id: int, expiry_days: int = 30):
    inbound_id = 2
    expiry_ts = int((datetime.utcnow() + timedelta(days=expiry_days)).timestamp()) * 1000
    client_id = str(uuid.uuid4())
    remark = f"user_{telegram_id}_{tx_id}"
    email = f"{telegram_id}@speedvpn"

    clients_data = {
        "clients": [
            {
                "id": client_id,
                "flow": "",
                "email": email,
                "limitIp": 1,
                "totalGB": 0,
                "expiryTime": expiry_ts,
                "enable": True,
                "tgId": str(telegram_id),
                "subId": str(tx_id),
                "comment": remark,
                "reset": 0
            }
        ]
    }

    payload = {
        "id": inbound_id,
        "settings": json.dumps(clients_data)
    }

    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            login_url = XUI_API_URL.rstrip("/") + "/login"
            login_data = {"username": XUI_USERNAME, "password": XUI_PASSWORD}
            async with session.post(login_url, data=login_data) as resp:
                login_text = await resp.text()
                if resp.status != 200 or "success" not in login_text.lower():
                    logger.error(f"❌ Ошибка авторизации в XUI ({resp.status}): {login_text}")
                    return {"id": 0, "link": "Ошибка: не удалось авторизоваться в XUI"}
                cookies = resp.cookies
                logger.info("✅ Авторизация успешна")

            add_url = XUI_API_URL.rstrip("/") + "/xui/API/inbounds/addClient"
            fallback_url = XUI_API_URL.rstrip("/") + "/panel/api/inbounds/addClient"

            logger.info(f"🚀 Пробуем основной endpoint: {add_url}")
            async with session.post(add_url, json=payload, cookies=cookies) as resp:
                add_text = await resp.text()
                logger.info(f"📩 Ответ addClient ({resp.status}): {add_text}")

                if resp.status != 200 or "success" not in add_text.lower():
                    logger.warning("⚠️ Основной endpoint не ответил корректно, пробуем fallback...")
                    async with session.post(fallback_url, json=payload, cookies=cookies) as resp2:
                        add_text = await resp2.text()
                        logger.info(f"📩 Ответ fallback addClient ({resp2.status}): {add_text}")

                        if resp2.status != 200 or "success" not in add_text.lower():
                            logger.error(f"❌ Ошибка при добавлении клиента: {add_text}")
                            return {"id": 0, "link": f"Ошибка при добавлении клиента ({resp2.status}): {add_text}"}

            list_url = XUI_API_URL.rstrip("/") + "/xui/API/inbounds/list"
            async with session.get(list_url, cookies=cookies) as resp:
                text = await resp.text()
                if not text:
                    logger.error("❌ XUI вернул пустой ответ")
                    return {"id": 0, "link": "Ошибка: XUI вернул пустой ответ"}
                data = json.loads(text)
                logger.info(f"📡 Ответ XUI /xui/API/inbounds/list ({resp.status}): получено {len(data.get('obj', []))} inbound'ов")

            inbound = next((i for i in data.get("obj", []) if i.get("id") == inbound_id), None)
            if not inbound:
                return {"id": 0, "link": f"Ошибка: inbound {inbound_id} не найден"}

            settings = json.loads(inbound.get("settings", "{}"))
            client_entry = next(
                (c for c in settings.get("clients", []) if c.get("email") == email),
                None
            )
            if not client_entry:
                return {"id": 0, "link": "Ошибка: клиент не найден в inbound"}

            security = "reality"
            pbk = "SKETCtsR8vCXdnMotgS8Q41BosktZRNqfH8T47XFhFg"
            sni = "yahoo.com"
            sid = "355b3003"
            fp = "chrome"
            port = 25300
            flow = client_entry.get("flow", "")
            remark_name = f"buy-{tx_id}"

            link = (
                f"vless://{client_entry['id']}@5.34.213.152:{port}"
                f"?type=tcp&security={security}&pbk={pbk}&fp={fp}"
                f"&sni={sni}&sid={sid}&spx=%2F"
                f"{'&flow=' + flow if flow else ''}"
                f"#{remark_name}"
            )

            logger.info(f"✅ Клиент успешно создан — реальная ссылка: {link}")

            StaticProfileHelper.add_profile(name=remark_name, vless_url=link)
            UserHelper.set_subscription(telegram_id, expiry_days)

            return {"id": client_entry['id'], "link": link}

    except Exception as e:
        logger.exception("❌ Ошибка при создании профиля через XUI API")
        return {"id": 0, "link": f"Ошибка: {e}"}
