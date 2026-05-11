@echo off
echo Обновление библиотек...
python -m pip install --upgrade pip
python -m pip install --upgrade pydantic aiogram
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo Сборка проекта...
python -m PyInstaller --onefile --noconsole --noconfirm --name "PC_Control_Bot" main.py

echo Очистка временных файлов сборки...
if exist dist\PC_Control_Bot.exe move /y dist\PC_Control_Bot.exe .\PC_Control_Bot.exe
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist PC_Control_Bot.spec del /q PC_Control_Bot.spec

echo Сборка завершена! Готовый файл: PC_Control_Bot.exe
pause
