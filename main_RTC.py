import time 
import board
import sdcardio
import storage
import busio
import adafruit_dht
import adafruit_pcf8523


I2C = busio.I2C(board.GP5, board.GP4)
rtc = adafruit_pcf8523.PCF8523(I2C)
dht = adafruit_dht.DHT22(board.GP15)

days = ("Sunday", "Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday")

#SPI SD_CS pin
SD_CS = board.GP17

#SPI setup for SD card
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
sdcard = sdcardio.SDCard(spi, SD_CS)
vfs = storage.VfsFat(sdcard)
try:
    storage.mount(vfs, "/sdcard")
    print("sd card mounted")
except ValueError:
    print("no SD card")

#set_time = False
set_time = True 

if set_time:
    t = time.struct_time((2023, 6, 23, 15, 39, 00, 1, -1, -1))
    print("Setting time to :", t)
    rtc.datetime = t
    print()

while True:
    t = rtc.datetime
    #print(t)

    print("The data is %s %d/%d/%d" % (days[t.tm_wday], t.tm_mon, t.tm_mday, t.tm_year))
    print("The time is %d:%02d%02d" % (t.tm_hour, t.tm_min, t.tm_sec))
    
    time.sleep(1)

def get_temp(sensor):
    temperature = dht.temperature
    return temperature

# initial write to the SD card on startup 
try:
    with open("/sdcard/temp.txt", "a") as f:
        # write the date
        f.write('The date is {} {}/{}/{}\n'.format(days[t.tm_wday],t.tm_mon, t.tm_mday, t.tm_year))
        # write the start time
        f.wirte('Temp, Time\n')
        # debug statement for REPL
        print("initial write to SD card complete, starting to log")
except ValueError:
    print("initial write to SD card failed - check card")

while True:
    try:
        t = rtc.datetime
        with open("/sdcard/temp.txt", "a") as f:
            temp = get_temp(temperature)
            f.write(' {},{}:{}:{}\n'.format(temp, t.tm_hour, t.tm_min, t.tm_sec))
            print("data written to sd card ")
        time.sleep(30)
    except ValueError:
        print("data error - cannot write to SD card")
        time.sleep(10)
