from aiogram import Router, F
from aiogram.types import Message
from utils import pc_control
import logging

router = Router()

@router.message(F.text & ~F.text.startswith('/'))
async def write_clipboard(message: Message):
    # Этот хэндлер сработает только если ни один другой хэндлер в предыдущих роутерах не подошел.
    # Поэтому нам больше не нужен список kb_commands.
    success = pc_control.set_clipboard(message.text)
    if success:
        await message.answer("✅ Текст скопирован в буфер обмена ПК!")
    else:
        await message.answer("❌ Не удалось скопировать текст в буфер обмена.")
