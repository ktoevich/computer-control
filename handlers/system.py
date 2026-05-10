from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os
from utils import pc_control

router = Router()

class BrowserState(StatesGroup):
    waiting_for_query = State()

@router.message(F.text == "📷 Фото с камеры")
async def handle_webcam_photo(message: Message):
    msg = await message.answer("📸 Делаю фото с веб-камеры...")
    path = pc_control.take_webcam_photo()
    if path:
        photo = FSInputFile(path)
        await message.answer_photo(photo)
        await msg.delete()
        os.remove(path)
    else:
        await msg.edit_text("❌ Не удалось получить доступ к веб-камере (возможно её нет или она занята).")

@router.message(F.text == "🎥 Видео с камеры")
async def handle_webcam_video(message: Message):
    msg = await message.answer("🎥 Записываю видео с веб-камеры (10 сек)...")
    path = pc_control.record_webcam_video()
    if path:
        video = FSInputFile(path)
        await message.answer_video(video)
        await msg.delete()
        os.remove(path)
    else:
        await msg.edit_text("❌ Не удалось получить доступ к веб-камере (возможно её нет или она занята).")

@router.message(F.text == "🔍 Поиск в браузере")
async def handle_browser_search_start(message: Message, state: FSMContext):
    await message.answer("Введите запрос или ссылку для открытия в браузере:\n(Для отмены введите любую другую команду клавиатуры)")
    await state.set_state(BrowserState.waiting_for_query)

@router.message(BrowserState.waiting_for_query)
async def handle_browser_query(message: Message, state: FSMContext):

    if message.text and message.text.startswith("/") or message.text in [
        "📸 Скриншот", "ℹ️ Статус", "📋 Буфер обмена", "📁 Открыть проводник"
    ]:
        await state.clear()
        await message.answer("Поиск отменен.")
        return
        
    url = pc_control.search_in_browser(message.text)
    await message.answer(f"🌐 Открыто в браузере ПК:\n`{url}`", parse_mode="Markdown")
    await state.clear()

@router.message(F.text == "🔌 Выключить")
async def handle_shutdown(message: Message):
    pc_control.shutdown_pc()
    await message.answer("⚠️ ПК будет выключен через 60 секунд. Нажмите '❌ Отмена выключения', если передумали.")

@router.message(F.text == "🔄 Перезагрузить")
async def handle_restart(message: Message):
    pc_control.restart_pc()
    await message.answer("⚠️ ПК будет перезагружен через 60 секунд. Нажмите '❌ Отмена выключения', если передумали.")

@router.message(F.text == "❌ Отмена выключения")
async def handle_cancel_shutdown(message: Message):
    pc_control.cancel_shutdown()
    await message.answer("✅ Выключение / Перезагрузка отменены.")

@router.message(F.text == "🔒 Заблокировать")
async def handle_lock(message: Message):
    pc_control.lock_pc()
    await message.answer("🔒 ПК заблокирован.")

@router.message(F.text == "💡 Монитор выкл")
async def handle_monitor_off(message: Message):
    pc_control.monitor_off()
    await message.answer("💡 Монитор выключен.")

@router.message(F.text == "⌨️ Win+D")
async def handle_win_d(message: Message):
    pc_control.win_d()
    await message.answer("💻 Все окна свернуты/развернуты.")

@router.message(F.text == "📁 Открыть проводник")
async def handle_explorer(message: Message):
    pc_control.open_explorer()
    await message.answer("📁 Проводник открыт на ПК.")

@router.message(F.text == "🌐 Открыть браузер")
async def handle_browser(message: Message):
    pc_control.open_browser()
    await message.answer("🌐 Браузер открыт на ПК.")

@router.message(F.text == "🖥 Диспетчер задач")
async def handle_taskmgr(message: Message):
    pc_control.open_task_manager()
    await message.answer("🖥 Диспетчер задач открыт.")

@router.message(F.text == "🧹 Очистить temp")
async def handle_cleartemp(message: Message):
    msg = await message.answer("Начинаю очистку временных файлов (Temp)...")
    result = pc_control.clear_temp()
    await msg.edit_text(result)
