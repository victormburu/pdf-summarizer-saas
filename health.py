import datetime
import psutil


battery = psutil.sensors_battery()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
remaining = now + datetime.timedelta(seconds=battery.secsleft) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "unlimited"
report = {
    "time": now,
    "battery": battery.percent,
    "is_plugged": battery.power_plugged,
    "is_charging": battery.power_plugged and battery.percent < 100,
    "is_discharging": not battery.power_plugged and battery.percent < 100,
    "is_full": battery.percent == 100,
    "time left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else remaining,
}

print(report)