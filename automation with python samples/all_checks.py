import socket

def check_root_full():
    return check_disk_full(disk="/", min_gb=2, min_percent=10)

def check_no_network():
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def main():
    checks = [
    (check_reboot, "pending reboot"),
    (check_root_full, "root partition full"),
    (check_no_network, "no working network")
    ]
