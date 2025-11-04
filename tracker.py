import psutil
from datetime import datetime

def check_dota_running():
    """Return True if dota2.exe is running"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == "dota2.exe":
            return True
    return False

def kill_dota():
    """Kill dota2.exe if running"""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == "dota2.exe":
            proc.kill()
            return True
    return False
