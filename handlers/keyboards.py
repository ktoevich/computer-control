from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📸 Скриншот"), KeyboardButton(text="📺 Трансляция экрана")],
            [KeyboardButton(text="ℹ️ Статус"), KeyboardButton(text="🌐 IP ПК")],
            [KeyboardButton(text="🔍 Поиск в браузере"), KeyboardButton(text="⌨️ Alt+Tab")],
            [KeyboardButton(text="📁 Открыть проводник"), KeyboardButton(text="📋 Буфер обмена")],
            [KeyboardButton(text="📷 Фото с камеры"), KeyboardButton(text="🎥 Видео с камеры")],
            [KeyboardButton(text="🔊 Громкость +"), KeyboardButton(text="🔉 Громкость -")],
            [KeyboardButton(text="🖥 Диспетчер задач"), KeyboardButton(text="⌨️ Win+D")],
            [KeyboardButton(text="🧹 Очистить temp"), KeyboardButton(text="🔒 Заблокировать")],
            [KeyboardButton(text="🔄 Перезагрузить"), KeyboardButton(text="🔌 Выключить")],
            [KeyboardButton(text="⏸ Пауза музыки"), KeyboardButton(text="🔇 Мут")],
            [KeyboardButton(text="⏮ Пред. трек"), KeyboardButton(text="⏭ След. трек")],
            [KeyboardButton(text="📂 Файловый менеджер")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_typing_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⌨️ Enter"), KeyboardButton(text="⌨️ Backspace")],
            [KeyboardButton(text="⌨️ Space"), KeyboardButton(text="⌨️ Alt+Tab")],
            [KeyboardButton(text="⌨️ Win+D"), KeyboardButton(text="⌨️ Esc")],
            [KeyboardButton(text="❌ Выйти из режима ввода")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_streaming_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⌨️ Alt+Tab"), KeyboardButton(text="⌨️ Win+D")],
            [KeyboardButton(text="⌨️ Enter"), KeyboardButton(text="⌨️ Backspace")],
            [KeyboardButton(text="🛑 Остановить трансляцию")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_file_manager_keyboard(drives=None, files=None, current_path=""):
    pass
