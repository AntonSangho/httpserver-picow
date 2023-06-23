import time
import os
import board
import busio
import sdcardio
import storage
import digitalio
import adafruit_sdcard
#import microcontroller
import adafruit_dht

dht = adafruit_dht.DHT22(board.GP15)
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
cs = board.GP17
sdcard = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sdcard")

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# print("Logging temperature to filesystem")
# while True:
#     try:
#         temperature = dht.temperature
#         humidity = dht.humidity
#         print("Temp: {:.1f} *C \t Humidity: {}%".format(temperature, humidity))
#     except RuntimeError as e:
#         print("Reading from DHT failure: ", e.args)
#     time.sleep(1)

# append to the file!
while True:
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        #print("Temp: {:.1f} *C \t Humidity: {}%".format(temperature, humidity))
    except RuntimeError as e:
        print("Reading from DHT failure: ", e.args)
    time.sleep(1)

    # open file for append
    with open("/sdcard/temperature.txt", "a") as f:
        led.value = True  # turn on LED to indicate we're writing to the file
        #t = microcontroller.cpu.temperature
        t = temperature
        print("Temperature = %0.1f" % t)
        f.write("%0.1f\n" % t)
        led.value = False  # turn off LED to indicate we're done
    # file is saved
    time.sleep(1)


def print_directory(path, tabs=0):
    for file in os.listdir(path):
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000

        if filesize < 1000:
            sizestr = str(filesize) + " by"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize / 1000)
        else:
            sizestr = "%0.1f MB" % (filesize / 1000000)

        prettyprintname = ""
        for _ in range(tabs):
            prettyprintname += "   "
        prettyprintname += file
        if isdir:
            prettyprintname += "/"
        print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))

        # recursively print directory contents
        if isdir:
            print_directory(path + "/" + file, tabs + 1)


print("Files on filesystem:")
print("====================")
print_directory("/sdcard")
