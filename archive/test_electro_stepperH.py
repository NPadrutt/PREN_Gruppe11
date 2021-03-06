from src.StepperH import StepperH
from src.ElectroMagnet import ElectroMagnet
import time
import RPi.GPIO as GPIO

# starts horizontal stepper as thread
if __name__ == '__main__':
    stepper = StepperH()
    magnet = ElectroMagnet()

    try:
        stepper.start()
        time.sleep(2.5)
        magnet.start()
        while True:
            pass
    except(KeyboardInterrupt, SystemExit):
        magnet.clean_up()
        stepper.clean_up()
    magnet.join()
    stepper.join()
    GPIO.cleanup()
