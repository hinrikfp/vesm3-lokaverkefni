from microdot import Microdot, Response, send_file, redirect
from microdot_utemplate import render_template
from neopixel import NeoPixel
from machine import Pin, ADC, PWM
from time import sleep_ms, localtime
from math import cos, sin, acos, asin, degrees, radians
import network
from espnow import ESPNow
from machine import Timer
from servo import myServo
import json

moisture_adc = ADC(Pin(9), atten=ADC.ATTN_11DB)
light_adc = ADC(Pin(8), atten=ADC.ATTN_11DB)

servo = myServo(pin=21, hz=50)

ssidRouter = "TskoliVESM"
passwordRouter = "Fallegurhestur"

sta_if = network.WLAN(network.STA_IF)
#sta_if.config(channel=6)

print("channel:", sta_if.config("channel"))
def STA_Setup(ssidRouter,passwordRouter):
    print("setting soft-sta")
    if not sta_if.isconnected():
        print("connecting to", ssidRouter)
        sta_if.active(True)
        sta_if.connect(ssidRouter,passwordRouter)
        while not sta_if.isconnected():
            pass
    print("Connected, ip address:", sta_if.ifconfig())
    
try:
    STA_Setup(ssidRouter,passwordRouter)
except Exception as error:
    sta_if.disconnect()
    print("error ", error)
    raise error

# Initialize ESP-NOW
espnow = ESPNow()
espnow.active(True)

# MAC address of Device 2
peer = b'\xf4\x12\xfa\xff\xf8\x00'  # breyttu hér  MAC address
espnow.add_peer(peer)

def recv_cb(espnow):
    while True:  # Read out all messages waiting in the buffer
        mac, msg = espnow.irecv(0)  # Don't wait if no messages left
        if mac is None:
            return
        print(mac, msg)
espnow.irq(recv_cb)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)


def declination(day):
    DECL_CONST = -23.45
    return radians(DECL_CONST * cos((360/365)*(day + 10)))

def hour_angle(solar_time):
    DEG_CONST = 15
    return radians(15 * (solar_time - 12))

def solar_zenith(lat, solar_decl, hour_angl):
    zenith = (asin( sin(solar_decl) * sin(lat) + cos(solar_decl) * cos(lat) * cos(hour_angl)))
    return zenith

def solar_azimuth(lat, solar_decl, hour_angl, elevation):
    azimuth = degrees( acos( (sin(solar_decl) * cos(lat) - cos(solar_decl) * sin(lat) * cos(hour_angl) ) / cos(elevation) ) )
    if hour_angl < 0:
        return azimuth
    else:
        return (360 - azimuth)
    
latitude = 64
longitude = -23
    
def get_azimuth():
    global latitude
    global azimuth
    global zenith
    day = localtime()[-1]
    time = localtime()[3]
    zenith = (solar_zenith(latitude, declination(day), hour_angle(time)))
    azimuth = (solar_azimuth(latitude,declination(day),hour_angle(time),zenith))-23
    return azimuth
    
def hourly(time):
    global azimuth
    azimuth = get_azimuth()
    servo.writeAngle(azimuth)

def every_minute(time):
    global peer
    light = light_adc.read_u16()
    moisture = moisture_adc.read_u16()
    msg_dict = {"moisture": moisture, "light": light}
    msg_json = json.dumps(msg_dict)
    espnow.send(peer, msg_json)
    print("sent via espnow")

azimuth_timer = Timer(0)
azimuth_timer.init(period=(1800*1000), mode=Timer.PERIODIC, callback = hourly)
hourly(1)

minute_timer = Timer(1)
minute_timer.init(period=(3*1000), mode=Timer.PERIODIC, callback=every_minute)
every_minute(1)

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
def index(request):
    global azimuth
    moisture = moisture_adc.read_u16()
    light = light_adc.read_u16()
    yearday = localtime()[-1]
    return render_template('index.html', moisture=moisture, light=light, azimuth=azimuth)

@app.route('/changelat', methods=['GET','POST'])
def changelat(request):
    global latitude
    if request.form:
        try:
            new_lat = request.form.get("newlat")
            latitude = float(new_lat)
            print("new lat", new_lat)
            hourly()
        except Exception as e:
            print("error: ", e)
    redirect("/")
    
app.run(debug=True)


