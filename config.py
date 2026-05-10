import json
import os
import sys

CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Ошибка чтения config.json. Файл будет перезаписан.")

    print("=== Первоначальная настройка бота ===")
    print("Бот будет управлять вашим ПК, поэтому доступ должен быть только у вас.")
    token = input("Введите токен бота (от @BotFather): ").strip()
    
    while True:
        admin_id_str = input("Введите ваш Telegram ID (можно узнать у @userinfobot): ").strip()
        if admin_id_str.isdigit():
            admin_id = int(admin_id_str)
            break
        else:
            print("Telegram ID должен состоять только из цифр. Попробуйте еще раз.")

    config = {
        "BOT_TOKEN": token,
        "ADMIN_ID": admin_id
    }

    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    
    print("Настройки сохранены в config.json!")
    return config

config_data = load_config()

BOT_TOKEN = config_data.get("BOT_TOKEN", "")
ADMIN_ID = config_data.get("ADMIN_ID", 0)

if not BOT_TOKEN or not ADMIN_ID:
    print("Ошибка: Токен бота или ID администратора не заданы. Удалите config.json и перезапустите.")
    sys.exit(1)
