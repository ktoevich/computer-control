from aiogram import Router, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os
import logging
from utils import pc_control

router = Router()

class BrowserState(StatesGroup):
    waiting_for_query = State()
    typing_mode = State()

class LiveScreenState(StatesGroup):
    is_streaming = State()

@router.message(F.text.startswith("📷 Фото с камеры"))
async def handle_webcam_photo(message: Message):
    # Пытаемся извлечь индекс, если он есть (например "📷 Фото с камеры 1")
    args = message.text.split()
    index = None
    if len(args) > 3:
        try:
            index = int(args[-1])
        except ValueError:
            pass
            
    msg = await message.answer(f"📸 Делаю фото с камеры {index if index is not None else '(авто)'}...")
    path = pc_control.take_webcam_photo(camera_index=index)
    
    if path:
        photo = FSInputFile(path)
        await message.answer_photo(photo)
        await msg.delete()
        os.remove(path)
    else:
        await msg.edit_text("❌ Не удалось получить доступ к этой камере.")

@router.message(F.text.startswith("🎥 Видео с камеры"))
async def handle_webcam_video(message: Message):
    args = message.text.split()
    index = None
    if len(args) > 3:
        try:
            index = int(args[-1])
        except ValueError:
            pass
            
    msg = await message.answer(f"🎥 Записываю видео с камеры {index if index is not None else '(авто)'} (10 сек)...")
    path = pc_control.record_webcam_video(camera_index=index)
    
    if path:
        video = FSInputFile(path)
        await message.answer_video(video)
        await msg.delete()
        os.remove(path)
    else:
        await msg.edit_text("❌ Не удалось получить доступ к этой камере.")

@router.message(F.text == "/cameras")
async def handle_list_cameras(message: Message):
    cameras = pc_control.get_available_cameras()
    if not cameras:
        await message.answer("❌ Доступные камеры не найдены.")
    else:
        text = "📸 **Доступные камеры:**\n\n"
        for idx in cameras:
            text += f"🔹 Камера {idx}\n"
        text += "\nЧтобы использовать конкретную камеру, отправьте:\n`📷 Фото с камеры <номер>`"
        await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "🔍 Поиск в браузере")
@router.message(F.text == "⌨️ Удаленный ввод")
async def handle_browser_search_start(message: Message, state: FSMContext):
    from handlers.keyboards import get_typing_keyboard
    await message.answer("🌐 Режим удаленного ввода активен.\n\n"
                         "🔹 Если вы отправите ссылку или поисковый запрос, он откроется в браузере.\n"
                         "🔹 Все последующие сообщения будут напечатаны на ПК как текст.\n"
                         "🔹 Используйте кнопки для специальных клавиш.", 
                         reply_markup=get_typing_keyboard())
    await state.set_state(BrowserState.waiting_for_query)

@router.message(BrowserState.waiting_for_query)
async def handle_browser_query(message: Message, state: FSMContext):
    if message.text == "❌ Выйти из режима ввода":
        await state.clear()
        from handlers.keyboards import get_main_keyboard
        await message.answer("🚪 Режим ввода завершен.", reply_markup=get_main_keyboard())
        return
        
    # Если это первый ввод, пробуем открыть браузер
    url = pc_control.search_in_browser(message.text)
    await message.answer(f"🌐 Открыто/Напечатано: `{url}`\nТеперь вы можете отправлять текст для печати на ПК.", parse_mode="Markdown")
    await state.set_state(BrowserState.typing_mode)

@router.message(BrowserState.typing_mode)
async def handle_remote_typing(message: Message, state: FSMContext):
    if message.text == "❌ Выйти из режима ввода":
        await state.clear()
        from handlers.keyboards import get_main_keyboard
        await message.answer("🚪 Режим ввода завершен.", reply_markup=get_main_keyboard())
        return
        
    if message.text.startswith("⌨️ "):
        key = message.text.replace("⌨️ ", "").lower()
        if key == "alt+tab":
            pc_control.alt_tab()
        elif key == "win+d":
            pc_control.win_d()
        else:
            pc_control.press_key(key)
        await message.answer(f"✅ Нажато: `{key}`", parse_mode="Markdown")
        return

    pc_control.type_text(message.text)
    await message.answer(f"⌨️ Напечатано: `{message.text}`", parse_mode="Markdown")

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

@router.message(F.text == "⌨️ Alt+Tab")
async def handle_alt_tab(message: Message):
    pc_control.alt_tab()
    await message.answer("🔄 Выполнено Alt+Tab.")

@router.message(F.text == "📺 Трансляция экрана")
async def handle_live_screen_start(message: Message, state: FSMContext):
    await state.set_state(LiveScreenState.is_streaming)
    from handlers.keyboards import get_streaming_keyboard
    await message.answer("📺 Трансляция экрана запущена.\nЯ буду присылать скриншот каждые 4 секунды.\n\nВы можете использовать кнопки управления ниже или отправить текст для печати.",
                         reply_markup=get_streaming_keyboard())
    
    # Запускаем цикл отправки скриншотов
    import asyncio
    from aiogram.types import InputMediaPhoto
    
    path = pc_control.take_screenshot("live_screen.png")
    if not path:
        await message.answer("❌ Не удалось сделать скриншот.")
        await state.clear()
        return
        
    main_msg = await message.answer_photo(FSInputFile(path), caption="📺 Прямой эфир...")
    os.remove(path)

    while await state.get_state() == LiveScreenState.is_streaming:
        await asyncio.sleep(3) # Интервал обновления
        path = pc_control.take_screenshot("live_screen_update.png")
        if path:
            try:
                # Обновляем фото в том же сообщении
                await main_msg.edit_media(
                    media=InputMediaPhoto(media=FSInputFile(path), caption="📺 Прямой эфир (обновляется)...")
                )
                os.remove(path)
            except Exception as e:
                logging.error(f"Ошибка трансляции: {e}")
                # Если сообщение удалено или ошибка, пробуем отправить заново
                try:
                    main_msg = await message.answer_photo(FSInputFile(path), caption="📺 Прямой эфир...")
                    os.remove(path)
                except:
                    break
        else:
            break

@router.message(F.text == "🛑 Остановить трансляцию")
async def handle_live_screen_stop(message: Message, state: FSMContext):
    await state.clear()
    from handlers.keyboards import get_main_keyboard
    await message.answer("🛑 Трансляция остановлена.", reply_markup=get_main_keyboard())

@router.message(LiveScreenState.is_streaming)
async def handle_live_screen_typing(message: Message, state: FSMContext):
    if message.text.startswith("⌨️ "):
        key = message.text.replace("⌨️ ", "").lower()
        if key == "alt+tab":
            pc_control.alt_tab()
        elif key == "win+d":
            pc_control.win_d()
        else:
            pc_control.press_key(key)
        return
    
    pc_control.type_text(message.text)

@router.message(F.text == "🧹 Очистить temp")
async def handle_cleartemp(message: Message):
    msg = await message.answer("Начинаю очистку временных файлов (Temp)...")
    result = pc_control.clear_temp()
    await msg.edit_text(result)
