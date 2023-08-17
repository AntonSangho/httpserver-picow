# SPDX-FileCopyrightText: 2022 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import board
import os
import microcontroller
import ipaddress
import wifi
import socketpool
from adafruit_httpserver import Server, Request, Response, POST, FileResponse
import adafruit_dht
import time

dht = adafruit_dht.DHT22(board.GP15)

print("Connecting to WiFi")

#  connect to your SSID
#wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

#  set static IP address
ipv4 =  ipaddress.IPv4Address("192.168.1.45")
netmask =  ipaddress.IPv4Address("255.255.255.0")
gateway =  ipaddress.IPv4Address("192.168.1.1")
wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/www", debug=True)
unit = "C"
# font for HTML
font_family ="monospace"

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

#  pings Google
ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))


temperature = dht.temperature
humidity = dht.humidity
#  the HTML script
#  setup as an f string
#  this way, can insert string variables from code.py directly
#  of note, use {{ and }} if something from html *actually* needs to be in brackets
#  i.e. CSS style formatting
def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <body>
    <title>Pico W HTTP Server</title>
    <h1>Pico W HTTP Server</h1>
    <p>Temperature: {temperature:.2f}{unit}</p>
    <p>Humidity: {humidity:.2f}</p>
    </body>
    </html>
    """
    return html

    #  route default static IP
#server.route("/")
#def base(request: Request):  # pylint: disable=unused-argument
      ##serve the HTML f string
      ##with content type text/html
    #return FileResponse(request, "index.html","/www" )

# Start the server.
@server.route("/")
def base(request: Request):
    return Response(request, f"{webpage()}", content_type='text/html') 

server.serve_forever(str(wifi.radio.ipv4_address))

clock = time.monotonic # holder for server ping


#print("starting server...")
## start the server 
try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
    ## if the server fail to begin, restart pico
except OSError:
    time.sleep(5)
    print("restarting..")
    microcontroller.reset()
ping_address = ipaddress.ip_address("8.8.4.4")

while True:
    try:
        #  every 30 seconds, ping server & update temp reading
        if (clock + 30) < time.monotonic():
            if wifi.radio.ping(ping_address) is None:
                print("lost connection")
            else:
                print("connected")
            clock = time.monotonic()
            temperature = dht.temperature
            humidity = dht.humidity
            print("Temp: {:.1f} *C \t Humidity: {}%".format(temperature, humidity))
            server.poll()
    # pylint: disable=broad-except
    except Exception as e:
        print(e)
        continue
#while True:
    #try:
        #temperatrue = dht.temperature
        #print("Temp: {:.1f} *C ".format(temperatrue))
    #except RuntimeError as e:
        #print("Reading from DHT failure", e.args)
    #time.sleep(1)

