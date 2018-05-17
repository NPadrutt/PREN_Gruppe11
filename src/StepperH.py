from time import sleep
from StateMachine import StateMachine
import math
import RPi.GPIO as GPIO
from Observable import Observable
from multiprocessing import Value

DIR = 24  # Direction GPIO Pin
STEP = 23  # Step GPIO Pin
CW = 1  # Clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 1000  # Steps per Revolution (360 / 7.5)

step_count = SPR

class StepperH(Observable):
    _states = ['initialized', 'running_forwards', 'running_backwards', 'stopped']
    position = [0, 0]

    def __init__(self, has_found):
        print("[ StepperH ] initialising")

        self.has_found = has_found

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.output(DIR, CCW)

        Observable.__init__(self)
        self.amount_of_steps = 0
        self.steps_taken = 1
        self.delay = 0.06
        self.count = 5
        self.running = True # to stop stepper from main thread in the end

        self.sm = StateMachine.get_stepperh_machine(self, StepperH._states)
        print("[ StepperH ] Set delay between steps to " + str(self.delay) + "s")
        print("[ StepperH ] initialized")

    def run_to_cargo(self, amount_of_steps):
        self.amount_of_steps = amount_of_steps
        print("[ StepperH ] ON")
        print("[ StepperH ] Steps taken: " + str(self.steps_taken))
        print("[ StepperH ] Steps to take: " + str(self.amount_of_steps))

        self.delay = 0.06
        self.count = 5

        while self.steps_taken < self.amount_of_steps:
            self.do_steps(0.0003)

        print("[ StepperH ] OFF")
        print("[ StepperH ] Stepper took " + str(self.steps_taken) + " before stopping")
        print("[ StepperH ] Waiting for state change")

        self.stop_stepperH() # Change state in State Machine

    def run_until_stopped(self):
        self.running = True
        print("[ StepperH ] Resume forwards until square found")
        print("[ StepperH ] ON")

        self.delay = 0.06
        self.count = 5

        print("[ StepperH ] Value has found: " + str(self.has_found.value))

        while self.running:
            has_found = self.has_found
            print("[ StepperH ] Value has found: " + str(has_found.value))
            if not has_found.value:
                self.do_steps(0.001)

        print("[ StepperH ] OFF")

    def on(self, amount_of_steps):
        self.amount_of_steps = amount_of_steps
        steps_tekken = 0
        print("[ StepperH ] ON")
        print("[ StepperH ] Steps taken: " + str(self.steps_taken))
        print("[ StepperH ] Steps to take: " + str(self.amount_of_steps))

        while steps_tekken < self.amount_of_steps:
            steps_tekken += 1
            self.do_steps(0.001)

        print("[ StepperH ] OFF")
        print("[ StepperH ] Stepper took " + str(self.steps_taken) + " before stopping")
        print("[ StepperH ] Waiting for state change")

    def run_until_collided(self, collision_button):
        self.running = True
        print("[ StepperH ] Resume forwards until collision")
        print("[ StepperH ] ON")

        self.delay = 0.06
        self.count = 5

        while self.running:
            self.do_steps_slow()

        print("[ StepperH ] OFF")
        print
        print
        print
        print("[ StepperH ] -------------- YOU HAVE ARRIVED AT YOUR FINAL DESTINATION ----------------")

    def stop_running(self):
        self.running = False
        self.stop_stepperH()

    def get_sm(self):
        return self.sm

    def do_steps(self, delay):
        if self.delay > delay:
            self.delay = math.exp(-self.count) + 0.0005
            self.count = self.count + 0.01

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

        GPIO.output(STEP, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(self.delay)
        self.steps_taken += 1
        self.update_position()
        Observable.dispatch(self, str(self.get_x()) + ";" + str(self.get_y()))

    def do_steps_slow(self):
        if self.delay > 0.001:
            self.delay = math.exp(-self.count) + 0.0005
            self.count = self.count + 0.0075

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

        GPIO.output(STEP, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(self.delay)
        self.steps_taken += 1
        self.update_position()
        print("[ StepperH ] Steps taken: "+str(self.steps_taken))
        Observable.dispatch(self, str(self.get_x()) + ";" + str(self.get_y()))

    def update_position(self):
        self.position[0] += 1
        self.position[1] += 1

    def get_x(self):
        return self.position[0]

    def get_y(self):
        y_in_cm = (-2 * 10**-12 * self.position[0]**3) + 4 * 10**-7 * self.position[0]**2 + 0.0004 * self.position[0] + 35.508
        y_in_cm = y_in_cm - 7
        y_in_schritte = int(round(y_in_cm / 0.01570796))
        return y_in_schritte

    @staticmethod
    def clean_up():
        GPIO.cleanup()
