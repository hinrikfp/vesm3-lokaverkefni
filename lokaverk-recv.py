from machine import Pin
from neopixel import NeoPixel
from network import WLAN, STA_IF
from espnow import ESPNow
from time import sleep
from machine import Pin
import json

relay = Pin(10, Pin.OUT)

# NeoPixel initialization
neo = NeoPixel(Pin(48), 1)
def light_up(color):
    neo[0] = color
    neo.write()

# Initialize the wireless interface
sta = WLAN(STA_IF)
sta.active(True)
sta.config(channel=5)

# Initialize ESP-NOW
espnow = ESPNow()
espnow.active(True)

# MAC address of Device 1
peer = b'4\x85\x18\xacjL'  # breyttu addressu
espnow.add_peer(peer)

print("channel: ",sta.config("channel"))

def recv_cb(espnow):
    while True:  # Read out all messages waiting in the buffer
        mac, msg = espnow.irecv(0)  # Don't wait if no messages left
        print(mac)
        if mac is None:
            return
        message = msg.decode()
        message_dict = json.loads(message)
        print(message)
        if int(message_dict["moisture"]) < 35000:
            print("relay on")
            relay.value(1)
        else:
            relay.value(0)
        #if int(msg.decode()) < 30000:
        #    espnow.send("0 0 255")
espnow.irq(recv_cb)

while True:
    pass