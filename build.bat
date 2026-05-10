@echo off
echo Установка PyInstaller...
.\venv\Scripts\python.exe -m pip install pyinstaller

echo Сборка проекта...
.\venv\Scripts\pyinstaller.exe --onefile --name "PC_Control_Bot" main.py

echo Очистка временных файлов сборки...
move /y dist\PC_Control_Bot.exe .\PC_Control_Bot.exe
rmdir /s /q build
rmdir /s /q dist
del /q PC_Control_Bot.spec

echo Сборка завершена! Готовый файл: PC_Control_Bot.exe
pause
