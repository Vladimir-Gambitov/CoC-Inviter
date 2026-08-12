import os
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from config import CHAT_ID, CLAN_TAG
from coc_api import get_clan_members
from database import add_user

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    guide_photo_path = "guide.jpg"

    text = (
        f"👋 Привет, викинг!\n\n"
        f"Чтобы получить одноразовую ссылку на вход в наш чат, тебе нужно подтвердить, что ты состоишь в клане.\n\n"
        f"📌 Инструкция:\n"
        f"1. Зайди в Clash of Clans и открой свой профиль.\n"
        f"2. Найди свой тег игрока (как показано на скриншоте ниже).\n"
        f"3. Отправь мне свой тег в ответном сообщении.\n\n"
        f"👇 Пример того, что нужно написать:\n"
        f"#2ABC1234"
    )

    if os.path.exists(guide_photo_path):
        photo = FSInputFile(guide_photo_path)
        await message.answer_photo(photo=photo, caption=text, parse_mode="Markdown")
    else:
        await message.answer(text, parse_mode="Markdown")


@router.message(F.text)
async def process_player_tag(message: Message):
    raw_text = message.text.strip().upper()
    
    # Фильтруем обычный текст: обрабатываем только похожее на тег (# в начале или 6-12 букв/цифр)
    if not (raw_text.startswith("#") or (len(raw_text) >= 6 and raw_text.isalnum())):
        return

    # Заменяем букву O на 0 (в CoC тегах нет буквы O) и добавляем # в начало при отсутствии
    user_tag = raw_text.replace("O", "0")
    if not user_tag.startswith("#"):
        user_tag = f"#{user_tag}"

    await message.answer(f"Проверяю тег {user_tag} в составе клана...", parse_mode="Markdown")

    members = await get_clan_members(CLAN_TAG)

    found_player = None
    for player in members:
        # Приводим тег из API к нормализованному виду (O -> 0) для надежного сравнения
        player_tag = player.get('tag', '').upper().replace("O", "0")
        if player_tag == user_tag:
            found_player = player
            break

    if not found_player:
        await message.answer(
            "Игрок с таким тегом не найден, убедись что ты вступил в клан и проверь правильность тега!",
            parse_mode="Markdown"
        )
        return

    await add_user(message.from_user.id, found_player['tag'])

    try:
        invite_link = await message.bot.create_chat_invite_link(
            chat_id=CHAT_ID,
            member_limit=1
        )

        player_name = found_player['name']

        await message.answer(
            f"<b>✅ Успешно! Ты найден в клане.</b>\n\n"
            f"👤 Игровой ник: <b>{player_name}</b>\n\n"
            f"🔗 Твоя одноразовая ссылка для входа в чат:\n"
            f"{invite_link.invite_link}",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(
            f"⚠️ Твой тег подтвержден, но не удалось создать ссылку.\n"
            f"Убедись, что бот добавлен в чат и имеет права Администратора!\n\n"
            f"Ошибка: {e}"
        )
