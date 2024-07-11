import RPi.GPIO as GPIO            #library GPIO
import time

# #deklarasi variabel GPIO

#Deklarasi pin GPIO pada raspberry
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
relay=7
GPIO.setup(relay, GPIO.OUT)        #RELAY Aktif low

try:
    while True:
        GPIO.output(relay,GPIO.LOW)
        print("relay off")
        time.sleep(3)
        GPIO.output(relay,GPIO.HIGH)
        print("relay on")
        time.sleep(3)
finally:
    GPIO.cleanup()