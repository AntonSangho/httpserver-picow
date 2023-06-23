
import os
import time
import busio
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import mdns
import ipaddress
import wifi
import socketpool
from adafruit_httpserver import Server, Request, Response, MIMETypes, FileResponse


displayio.release_displays()


SDA = board.GP8
SCL = board.GP9
i2c = busio.I2C(SCL, SDA)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

WIDTH = 128
HEIGHT = 64
CENTER_X = int(WIDTH/2)
CENTER_Y = int(HEIGHT/2)

# Display
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

#if(i2c.try_lock()):
#    print("i2c.scan(): " + str(i2c.scan()))
#    i2c.unlock()
##print()
#
splash = displayio.Group()
display.show(splash)

text = "192.168.0.179"
#ip_address = wifi.radio.ipv4_address
text_area = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
    #terminalio.FONT, text=ip_address, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
)
splash.append(text_area)

MIMETypes.configure(
    default_to="text/plain",
    keep_for=[".html"]
)

ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

@server.route("/home")
def home(request: Request):
    """
    Serves the file /www/home.html.
    """

    return FileResponse(request, "home.html", "/www")

@server.route("/")
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    return Response(request, "Hello from pico W HTTP Server!")
    #return Response(request, "home.html", "/www")

# Start server
server.serve_forever(str(wifi.radio.ipv4_address))

while True:
    pass
