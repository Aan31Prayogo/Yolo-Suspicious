import RPi.GPIO as GPIO            #library GPIO
import time

# #deklarasi variabel GPIO
relay=3

#Deklarasi pin GPIO pada raspberry
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay, GPIO.OUT)        #RELAY Aktif low
GPIO.output(relay,0)


while True:
    GPIO.output(relay,0)
    print("relay off")
    time.sleep(3)
    GPIO.output(relay,1)
    print("relay on")
    time.sleep(3)
