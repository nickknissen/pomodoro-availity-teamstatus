import pywinusb.hid as hid
from msvcrt import kbhit
from time import sleep
import requests
import json
import os

from dotenv import load_dotenv

currentState = "Available"

# DoNotDisturb, Available
def send_request(availability, auth_token):
    assert availability in ['DoNotDisturb', 'Available'], availability

    headers = {
        'authority': 'presence.teams.microsoft.com',
        'authorization': f'Bearer {auth_token}',
        'content-type': 'application/json',
        'accept': 'json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55',
        'origin': 'https://teams.microsoft.com',
        'referer': 'https://teams.microsoft.com/',
        'accept-language': 'da,en;q=0.9',
    }

    data = json.dumps({"availability": availability})

    return requests.put('https://presence.teams.microsoft.com/v1/me/forceavailability/', headers=headers, data=data)

def sample_handler(data):
    # red color
    #              min  seconds  stopped=1
    # [0, 146, 81, 39,  59,      0,          4, 0, 0] red
    # [0, 146, 81, 39,  31,      1,          4, 0, 0]

    #green color
    #               min  seconds  stopped
    # [0, 146, 82,  4,   9,       0,      4, 0, 0] 
    # [0, 146, 82,  4,   9,       1,      4, 0, 0] 

    #yellow
    #              min  seconds  stopped
    # [0, 146, 83,  9,   56,     0,         4, 0, 0]
    # [0, 146, 83,  9,   55,     1,         4, 0, 0]
    # [0, 146, 83,  9,   54,     0,         4, 0, 0]
    global currentState

    state = "DoNotDisturb" 

    if (data[2] == 82):
        state = "Available"

    if (data[2] == 83):
        state = "Available"

    currentState = state


if __name__ == "__main__":
    load_dotenv()

    VENDOR_ID = 0x04d8 #lux 
    PRODUCT_STRING = "LUXAFOR POMO"
    TEAMS_WEB_AUTH_TOKEN = os.getenv("TEAMS_WEB_AUTH_TOKEN")

    device = None
    all_devices = hid.HidDeviceFilter(vendor_id = VENDOR_ID).get_devices()
    device = all_devices[0]

    if device is None:
        print("Found no device")
        exit()

    try:
        device.open()
        #set custom raw data handler
        device.set_raw_data_handler(sample_handler)

        print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
        while not kbhit() and device.is_plugged():
            print("sending teams precense: {0}".format(currentState))
            response = send_request(currentState, TEAMS_WEB_AUTH_TOKEN)
            print("request status_code: {0}".format(response.status_code))
            assert response.status_code == 200, response.status_code 
            sleep(10)

    finally:
        device.close()
