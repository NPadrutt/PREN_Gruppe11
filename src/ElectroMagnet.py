# Libraries
import RPi.GPIO as GPIO
import threading
import time

# GPIO Output Pin
GPIO_TRIGGER = 12

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)


class ElectroMagnet(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
        print("\nElectromagnet ON")
        while self.running:
            print("Electromagnet still running...")
            time.sleep(5)

        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        print("\nElectromagnet OFF")
        GPIO.cleanup()