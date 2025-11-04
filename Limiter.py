import psutil
import time
from datetime import datetime

# Daily play limit (for now keep 30s test, later change to 3*60*60)
daily_limit = 30  
used_time = 0
last_checked = None
last_reset_date = None

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # Reset timer every day at 8:00 AM
    if now.hour == 8 and (last_reset_date is None or last_reset_date != now.date()):
        used_time = 0
        last_reset_date = now.date()
        print(f"[{current_time}] 🔄 Daily timer reset at 8 AM")

    # Check if dota2.exe is running
    running = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == "dota2.exe":
            running = True
            if last_checked:
                used_time += (now - last_checked).total_seconds()

            print(f"[{current_time}] Dota2 running | Time used: {int(used_time)}s")

            if used_time >= daily_limit:
                try:
                    proc.kill()
                    print(f"[{current_time}] ✅ Dota2 closed! Daily limit ({daily_limit}s) reached.")
                except Exception as e:
                    print(f"[{current_time}] ⚠️ Could not close process: {e}")

    if not running:
        print(f"[{current_time}] Dota2 not running | Time used: {int(used_time)}s")

    last_checked = now
    time.sleep(5)  # check every 5 seconds
