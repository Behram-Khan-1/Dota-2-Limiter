import psutil
import time
from datetime import datetime, timedelta
from logger import log_to_excel, get_last_played_time
import config

import os
import sys
import time
import subprocess

def restart_program():
    """ Relaunches this program """
    python = sys.executable
    os.execl(python, python, *sys.argv)

def main_loop():
   while True:
       try:
           import main   # or call your main() function directly
           main.main()
       except Exception as e:
           print(f"App crashed: {e}. Restarting in 5s...")
           time.sleep(5)
           restart_program()

def main():
    # ⏮ Load last saved played time from Excel (only if today's row exists)
    today_str = datetime.now().strftime("%Y-%m-%d")
    used_time = get_last_played_time(today_str)
    last_checked = None
    last_reset_date = datetime.now().date()
    last_log_time = time.time()  # for 5 min logging

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

       # 🔄 Daily reset check (works even if PC was off at reset hour)
        if now.date() != last_reset_date:
        # finalize yesterday’s log
            log_to_excel(today_str, used_time, "No")

            # reset for new day
            used_time = 0
            last_reset_date = now.date()
            today_str = now.strftime("%Y-%m-%d")
            print(f"[{current_time}] New day detected → counter reset.")


        # 🎮 Check if Dota2 is running
        dota_running = False
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == "dota2.exe":
                dota_running = True
                if last_checked:
                    used_time += (now - last_checked).total_seconds()

                # ⏱ If limit reached → close & log
                if used_time >= config.DAILY_LIMIT:
                    try:
                        proc.kill()
                        print(f"[{current_time}] [OK] Dota2 closed! Daily limit reached.")
                        log_to_excel(today_str, used_time, "Yes")
                    except Exception as e:
                        print(f"[{current_time}] Could not close process: {e}")

        # 📝 Log progress every 5 minutes
        if time.time() - last_log_time >= 300:  # 300 sec = 5 min
            log_to_excel(today_str, used_time, "No")
            last_log_time = time.time()

        if dota_running:
            print(f"[{current_time}] Dota2 running... Total today: {timedelta(seconds=int(used_time))}")

        last_checked = now
        time.sleep(5)  # check every 5 sec


if __name__ == "__main__":
    main_loop()
