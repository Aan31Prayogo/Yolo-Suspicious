import RPi.GPIO as GPIO  # library GPIO
import time
import atexit

# Deklarasi pin GPIO pada raspberry
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
relay = 7
GPIO.setup(relay, GPIO.OUT)  # RELAY Aktif low

# Function to cleanup GPIO and turn off relay
def cleanup_gpio():
    GPIO.output(relay, GPIO.LOW)
    GPIO.cleanup()

# Register the cleanup function to be called on exit
atexit.register(cleanup_gpio)

try:
    while True:
        GPIO.output(relay, GPIO.LOW)
        print("relay off")
        time.sleep(3)
        GPIO.output(relay, GPIO.HIGH)
        print("relay on")
        time.sleep(3)
except KeyboardInterrupt:
    pass

# Additional cleanup in case of normal program termination
cleanup_gpio()
