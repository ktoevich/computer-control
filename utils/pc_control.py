import os
import psutil
import pyautogui
import pyperclip
import keyboard
import socket
import subprocess
import ctypes
import tempfile
import shutil

def get_system_status():
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        battery = psutil.sensors_battery()
        bat_percent = battery.percent if battery else "Нет батареи"
        bat_plugged = "Подключена" if battery and battery.power_plugged else "Отключена"
        
        status = f"🖥 **Статус системы:**\n\n"
        status += f"🧠 **CPU:** {cpu}%\n"
        status += f"💾 **RAM:** {ram.percent}% ({ram.used // (1024**3)}GB / {ram.total // (1024**3)}GB)\n"
        if battery:
            status += f"🔋 **Батарея:** {bat_percent}% ({bat_plugged})\n"
        else:
            status += f"🔋 **Батарея:** {bat_percent}\n"
            
        return status
    except Exception as e:
        return f"Ошибка получения статуса: {e}"

def get_pc_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return f"🌐 **Локальный IP:** {local_ip}"
    except Exception as e:
        return f"Ошибка получения IP: {e}"

def take_screenshot(path="screenshot.png"):
    try:
        pyautogui.screenshot(path)
        return path
    except Exception as e:
        return None

def get_clipboard():
    try:
        return pyperclip.paste()
    except Exception as e:
        return f"Ошибка: {e}"

def set_clipboard(text):
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        return False

def take_webcam_photo(path="webcam.png"):
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        for _ in range(10):
            cap.read()
        ret, frame = cap.read()
        cap.release()
        if ret:
            cv2.imwrite(path, frame)
            return path
        return None
    except Exception:
        return None

def record_webcam_video(path="webcam_video.mp4", duration=10):
    try:
        import cv2
        import time
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0.0 or fps < 0:
            fps = 20.0
            
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(path, fourcc, fps, (width, height))
        
        start_time = time.time()
        while (time.time() - start_time) < duration:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break
                
        cap.release()
        out.release()
        return path
    except Exception:
        return None

def search_in_browser(query):
    import webbrowser
    import urllib.parse
    if query.startswith("http://") or query.startswith("https://"):
        url = query
    else:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return url

def media_play_pause():
    keyboard.send("play/pause media")

def media_next_track():
    keyboard.send("next track")

def media_prev_track():
    keyboard.send("previous track")

def volume_up():
    for _ in range(5):
        keyboard.send("volume up")

def volume_down():
    for _ in range(5):
        keyboard.send("volume down")

def volume_mute():
    keyboard.send("volume mute")

def win_d():
    keyboard.send("windows+d")

def open_explorer():
    subprocess.Popen('explorer')

def open_browser():
    subprocess.Popen('start msedge', shell=True)

def open_task_manager():
    subprocess.Popen('taskmgr')

def open_application(app_name_or_path):
    try:
        if os.path.exists(app_name_or_path):
            os.startfile(app_name_or_path)
            return True
        else:
            subprocess.Popen(app_name_or_path, shell=True)
            return True
    except Exception as e:
        return str(e)

def type_text(text):
    try:
        pyautogui.write(text, interval=0.05)
        return True
    except Exception as e:
        return str(e)

def press_key(key):
    try:
        pyautogui.press(key)
        return True
    except Exception as e:
        return str(e)

def press_hotkey(*keys):
    try:
        pyautogui.hotkey(*keys)
        return True
    except Exception as e:
        return str(e)
def shutdown_pc():
    os.system("shutdown /s /t 60")

def restart_pc():
    os.system("shutdown /r /t 60")

def cancel_shutdown():
    os.system("shutdown /a")

def lock_pc():
    ctypes.windll.user32.LockWorkStation()

def monitor_off():
    SC_MONITORPOWER = 0xF170
    HWND_BROADCAST = 0xFFFF
    WM_SYSCOMMAND = 0x0112
    ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)

def clear_temp():
    temp_dir = tempfile.gettempdir()
    deleted = 0
    errors = 0
    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
            deleted += 1
        except Exception:
            errors += 1
    return f"Очистка Temp завершена.\nУдалено: {deleted}\nОшибок: {errors}"
