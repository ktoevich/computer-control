from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📸 Скриншот"), KeyboardButton(text="ℹ️ Статус")],
            [KeyboardButton(text="📋 Буфер обмена"), KeyboardButton(text="📁 Открыть проводник")],
            [KeyboardButton(text="🌐 Открыть браузер"), KeyboardButton(text="💡 Монитор выкл")],
            [KeyboardButton(text="🔍 Поиск в браузере")],
            [KeyboardButton(text="📷 Фото с камеры"), KeyboardButton(text="🎥 Видео с камеры")],
            [KeyboardButton(text="🔊 Громкость +"), KeyboardButton(text="🔉 Громкость -")],
            [KeyboardButton(text="🖥 Диспетчер задач"), KeyboardButton(text="⌨️ Win+D")],
            [KeyboardButton(text="🧹 Очистить temp"), KeyboardButton(text="🔒 Заблокировать")],
            [KeyboardButton(text="🔄 Перезагрузить"), KeyboardButton(text="🔌 Выключить")],
            [KeyboardButton(text="❌ Отмена выключения")],
            [KeyboardButton(text="🔇 Мут"), KeyboardButton(text="⏸ Пауза музыки")],
            [KeyboardButton(text="⏭ Следующий трек"), KeyboardButton(text="⏮ Предыдущий трек")],
            [KeyboardButton(text="🧠 CPU"), KeyboardButton(text="💾 RAM")],
            [KeyboardButton(text="🔋 Батарея"), KeyboardButton(text="🌐 IP ПК")],
            [KeyboardButton(text="📂 Файловый менеджер")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_file_manager_keyboard(drives=None, files=None, current_path=""):
    pass
