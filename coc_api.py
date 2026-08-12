import aiohttp
from config import COC_API_TOKEN

async def get_clan_members(clan_tag: str):
    formatted_tag = clan_tag.replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/clans/{formatted_tag}/members"

    headers = {
        "Authorization": f"Bearer {COC_API_TOKEN}",
        "Accept": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            print(f"--- CoC API Запрос к {url} ---")
            print(f"Статус ответа: {response.status}")
            data = await response.json()
            
            if response.status == 200:
                members = data.get("items", [])
                print(f"Успешно получено участников: {len(members)}")
                if members:
                    print("Пример первого игрока:", members[0].get("name"), members[0].get("tag"))
                return members
            else:
                print(f"Ошибка от CoC API (Код {response.status}): {data}")
                return []
