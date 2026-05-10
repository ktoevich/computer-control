from aiogram import Router, F
from aiogram.types import Message
from utils import pc_control

router = Router()

@router.message(F.text == "🔊 Громкость +")
async def handle_vol_up(message: Message):
    pc_control.volume_up()
    await message.answer("🔊 Громкость увеличена.")

@router.message(F.text == "🔉 Громкость -")
async def handle_vol_down(message: Message):
    pc_control.volume_down()
    await message.answer("🔉 Громкость уменьшена.")

@router.message(F.text == "🔇 Мут")
async def handle_mute(message: Message):
    pc_control.volume_mute()
    await message.answer("🔇 Звук переключен (Мут/Размьют).")

@router.message(F.text == "⏸ Пауза музыки")
async def handle_play_pause(message: Message):
    pc_control.media_play_pause()
    await message.answer("⏯ Воспроизведение переключено.")

@router.message(F.text == "⏭ Следующий трек")
async def handle_next_track(message: Message):
    pc_control.media_next_track()
    await message.answer("⏭ Следующий трек.")

@router.message(F.text == "⏮ Предыдущий трек")
async def handle_prev_track(message: Message):
    pc_control.media_prev_track()
    await message.answer("⏮ Предыдущий трек.")
