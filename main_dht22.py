import board
import adafruit_dht
import time

dht = adafruit_dht.DHT22(board.GP15)

while True:
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        print("Temp: {:.1f} *C \t Humidity: {}%".format(temperature, humidity))
    except RuntimeError as e:
        print("Reading from DHT failure: ", e.args)
    time.sleep(1)