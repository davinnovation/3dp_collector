import os

def check_alive(ip_address):
    response = os.system("ping -c 1 "+ip_address)

    if response == 0:
        return True
    else:
        return False

