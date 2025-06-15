#!/usr/bin/env python   
import shutil
import psutil
from plyer import notification # library to send notifications to the user

def check_disk_usage(disk):
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > 20

def check_cpu_usage():
    usage = psutil.cpu_percent(1)
    return usage < 75

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

if not check_disk_usage("/") or not check_cpu_usage():
    print("ERROR!")
    # send a notification to the user
    send_notification("system Alert", "disk or CPU usage is to high")
else:
    print("Everything is OK!")
    # send a notification to the user
    send_notification("system Alert", "Everything is OK!")
