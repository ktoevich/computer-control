import os
import psutil
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command

router = Router()

USER_STATE = {
    'current_path': '',
    'items': [] 
}

def get_drives():
    drives = []
    for partition in psutil.disk_partitions():
        if 'cdrom' in partition.opts or partition.fstype == '':
            continue
        drives.append((partition.device, partition.device, True))
    return drives

def generate_fm_keyboard(items, current_path):
    builder = []
    
    if current_path != "":
        builder.append([InlineKeyboardButton(text="⬆️ Наверх", callback_data="fm:up"),
                        InlineKeyboardButton(text="💻 Этот ПК", callback_data="fm:drives")])
    
    for idx, (name, path, is_dir) in enumerate(items):
        icon = "📁" if is_dir else "📄"
        
        display_name = (name[:30] + '..') if len(name) > 30 else name
        
        if is_dir:
            builder.append([
                InlineKeyboardButton(text=f"{icon} {display_name}", callback_data=f"fm:nav:{idx}"),
                InlineKeyboardButton(text="⬇️ ZIP", callback_data=f"fm:zip:{idx}")
            ])
        else:
            builder.append([
                InlineKeyboardButton(text=f"{icon} {display_name}", callback_data=f"fm:file:{idx}")
            ])
        
    return InlineKeyboardMarkup(inline_keyboard=builder)

@router.message(F.text == "📂 Файловый менеджер")
async def fm_start(message: Message):
    USER_STATE['current_path'] = ""
    USER_STATE['items'] = get_drives()
    
    kb = generate_fm_keyboard(USER_STATE['items'], "")
    await message.answer("💻 **Этот компьютер**\nВыберите диск:", reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data.startswith("fm:"))
async def fm_callback(call: CallbackQuery):
    action = call.data.split(":")
    cmd = action[1]
    
    if cmd == "drives":
        USER_STATE['current_path'] = ""
        USER_STATE['items'] = get_drives()
        kb = generate_fm_keyboard(USER_STATE['items'], "")
        await call.message.edit_text("💻 **Этот компьютер**\nВыберите диск:", reply_markup=kb, parse_mode="Markdown")
        await call.answer()
        
    elif cmd == "up":
        current = USER_STATE['current_path']
        if not current:
            await call.answer("Вы уже в корне.")
            return
        
        parent = os.path.dirname(current)
        if parent == current or not current.strip("\\"):
            USER_STATE['current_path'] = ""
            USER_STATE['items'] = get_drives()
            kb = generate_fm_keyboard(USER_STATE['items'], "")
            await call.message.edit_text("💻 **Этот компьютер**\nВыберите диск:", reply_markup=kb, parse_mode="Markdown")
        else:
            await navigate_to(call, parent)
            
    elif cmd == "nav":
        idx = int(action[2])
        if idx < len(USER_STATE['items']):
            _, target_path, _ = USER_STATE['items'][idx]
            await navigate_to(call, target_path)
        else:
            await call.answer("Ошибка: папка не найдена")
            
    elif cmd == "file":
        idx = int(action[2])
        if idx < len(USER_STATE['items']):
            _, target_path, _ = USER_STATE['items'][idx]
            await call.answer("Отправка файла...")
            try:
                if os.path.getsize(target_path) > 50 * 1024 * 1024:
                    await call.message.answer("❌ Файл слишком большой (лимит Telegram - 50 МБ).")
                    return
                file = FSInputFile(target_path)
                await call.message.answer_document(file)
            except Exception as e:
                await call.message.answer(f"Ошибка при отправке файла: {e}")
        else:
            await call.answer("Ошибка: файл не найден")
            
    elif cmd == "zip":
        import tempfile
        import shutil
        idx = int(action[2])
        if idx < len(USER_STATE['items']):
            name, target_path, is_dir = USER_STATE['items'][idx]
            if not is_dir:
                await call.answer("Это не папка!")
                return
                
            await call.answer()
            msg = await call.message.answer(f"📦 Архивирую папку `{name}`. Пожалуйста, подождите...", parse_mode="Markdown")
            
            try:
                temp_dir = tempfile.gettempdir()
                zip_path_no_ext = os.path.join(temp_dir, f"folder_{name}")
                
                zip_path = shutil.make_archive(zip_path_no_ext, 'zip', target_path)
                
                if os.path.getsize(zip_path) > 50 * 1024 * 1024:
                    await msg.edit_text(f"❌ Архив получился слишком большим ({os.path.getsize(zip_path) // (1024*1024)} МБ). Лимит Telegram - 50 МБ.")
                    os.remove(zip_path)
                    return
                
                await msg.edit_text("Отправка архива...")
                file = FSInputFile(zip_path)
                await call.message.answer_document(file)
                await msg.delete()
                
                os.remove(zip_path)
                
            except Exception as e:
                await msg.edit_text(f"Ошибка при архивации или отправке: {e}")
                if 'zip_path' in locals() and os.path.exists(zip_path):
                    os.remove(zip_path)
        else:
            await call.answer("Ошибка: папка не найдена")

async def navigate_to(call: CallbackQuery, path: str):
    try:
        items = []
        with os.scandir(path) as it:
            for entry in it:
                items.append((entry.name, entry.path, entry.is_dir()))
        
        items.sort(key=lambda x: (not x[2], x[0].lower()))
        
        items = items[:80]

        USER_STATE['current_path'] = path
        USER_STATE['items'] = items
        
        kb = generate_fm_keyboard(items, path)
        await call.message.edit_text(f"📁 **Текущая папка:**\n`{path}`", reply_markup=kb, parse_mode="Markdown")
        await call.answer()
    except PermissionError:
        await call.answer("Нет доступа к этой папке!", show_alert=True)
    except Exception as e:
        await call.answer(f"Ошибка: {e}", show_alert=True)
        
@router.message(F.document)
async def handle_document(message: Message, bot):
    current_path = USER_STATE.get('current_path', '')
    if current_path == "":
        await message.answer("Сначала выберите папку в Файловом менеджере, куда нужно сохранить файл.")
        return
        
    doc = message.document
    file_id = doc.file_id
    file_name = doc.file_name
    dest_path = os.path.join(current_path, file_name)
    
    msg = await message.answer(f"Скачивание файла {file_name} в {current_path}...")
    try:
        await bot.download(doc, destination=dest_path)
        
        items = []
        with os.scandir(current_path) as it:
            for entry in it:
                items.append((entry.name, entry.path, entry.is_dir()))
        items.sort(key=lambda x: (not x[2], x[0].lower()))
        USER_STATE['items'] = items
        
        await msg.edit_text(f"✅ Файл успешно сохранен:\n`{dest_path}`", parse_mode="Markdown")
    except Exception as e:
        await msg.edit_text(f"❌ Ошибка при сохранении файла: {e}")
