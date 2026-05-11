import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from handlers.keyboards import get_main_keyboard
from utils import pc_control

router = Router()

@router.message(CommandStart())
async def start_cmd(message: Message):
    welcome_text = (
        "👋 Добро пожаловать! Бот для управления ПК запущен.\n"
        "Выберите действие на клавиатуре ниже, либо используйте команды:\n"
        "/app <имя или путь> - Открыть приложение/файл\n"
        "/type <текст> - Напечатать текст\n"
        "/key <кнопка> - Нажать клавишу (например, enter, space, a)\n"
        "/hotkey <кл1> <кл2> - Нажать комбинацию (например, ctrl c)\n"
        "/cameras - Список всех доступных камер\n"
    )
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "ℹ️ Статус")
async def handle_status(message: Message):
    status_text = pc_control.get_system_status()
    await message.answer(status_text, parse_mode="Markdown")

@router.message(F.text == "🧠 CPU")
async def handle_cpu(message: Message):
    import psutil
    cpu = psutil.cpu_percent(interval=1)
    await message.answer(f"🧠 **CPU Usage:** {cpu}%", parse_mode="Markdown")

@router.message(F.text == "💾 RAM")
async def handle_ram(message: Message):
    import psutil
    ram = psutil.virtual_memory()
    await message.answer(f"💾 **RAM Usage:** {ram.percent}% ({ram.used // (1024**3)}GB / {ram.total // (1024**3)}GB)", parse_mode="Markdown")

@router.message(F.text == "🔋 Батарея")
async def handle_battery(message: Message):
    import psutil
    battery = psutil.sensors_battery()
    if battery:
        plugged = "Подключена" if battery.power_plugged else "Отключена"
        await message.answer(f"🔋 **Батарея:** {battery.percent}% ({plugged})", parse_mode="Markdown")
    else:
        await message.answer("🔋 **Батарея:** Нет батареи", parse_mode="Markdown")

@router.message(F.text == "🌐 IP ПК")
async def handle_ip(message: Message):
    ip_text = pc_control.get_pc_ip()
    await message.answer(ip_text, parse_mode="Markdown")

@router.message(F.text == "📸 Скриншот")
async def handle_screenshot(message: Message):
    msg = await message.answer("Делаю скриншот...")
    path = pc_control.take_screenshot()
    if path:
        photo = FSInputFile(path)
        await message.answer_photo(photo)
        await msg.delete()
        os.remove(path)
    else:
        await msg.edit_text("Не удалось сделать скриншот.")

@router.message(F.text == "📋 Буфер обмена")
async def handle_clipboard(message: Message):
    clip_text = pc_control.get_clipboard()
    if not clip_text:
        await message.answer("Буфер обмена пуст.")
    else:
        await message.answer(f"📋 **В буфере обмена:**\n\n`{clip_text}`", parse_mode="Markdown")

@router.message(Command("app"))
async def handle_open_app(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Использование: `/app <имя_или_путь>`\nПример: `/app notepad`", parse_mode="Markdown")
        return
    app_name = args[1]
    result = pc_control.open_application(app_name)
    if result is True:
        await message.answer(f"✅ Запрос на открытие `{app_name}` выполнен.", parse_mode="Markdown")
    else:
        await message.answer(f"❌ Ошибка при открытии: {result}")

@router.message(Command("type"))
async def handle_type_text(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Использование: `/type <текст>`", parse_mode="Markdown")
        return
    text = args[1]
    result = pc_control.type_text(text)
    if result is True:
        await message.answer(f"✅ Текст напечатан.")
    else:
        await message.answer(f"❌ Ошибка при печати: {result}")

@router.message(Command("key"))
async def handle_press_key(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Использование: `/key <кнопка>`\nПример: `/key enter`", parse_mode="Markdown")
        return
    key = args[1].strip()
    result = pc_control.press_key(key)
    if result is True:
        await message.answer(f"✅ Нажата клавиша: `{key}`", parse_mode="Markdown")
    else:
        await message.answer(f"❌ Ошибка: {result}")

@router.message(Command("hotkey"))
async def handle_hotkey(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Использование: `/hotkey <клавиша1> <клавиша2>...`\nПример: `/hotkey ctrl c`", parse_mode="Markdown")
        return
    keys = args[1].split()
    result = pc_control.press_hotkey(*keys)
    if result is True:
        await message.answer(f"✅ Нажата комбинация: `{'+'.join(keys)}`", parse_mode="Markdown")
    else:
        await message.answer(f"❌ Ошибка: {result}")


