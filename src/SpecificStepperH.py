from time import sleep
from StateMachine import StateMachine
import math
import RPi.GPIO as GPIO
import threading

DIR = 24  # Direction GPIO Pin
STEP = 23  # Step GPIO Pin
CW = 1  # Clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 1000  # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# set direction forward (clockwise)
GPIO.output(DIR, CCW)

step_count = SPR
delay = .0005


class StepperH(threading.Thread):
    _states = ['initialized', 'running_forwards', 'running_backwards', 'stopped']
    position = [0, 0]

    def __init__(self):
        threading.Thread.__init__(self)
        self.steps = 0;
        self.lastStep = 0;
        self.delay = 0.05
        self.count = 5
        self.sm = StateMachine.get_stepperh_machine(self, StepperH._states)

    def run(self):
        print("\nStepperH ON")

        while self.is_running_forwards() and self.get_x() < 20:
            self.do_steps()

        self.clean_up()

        print("[StepperH]: Waiting for state change")
        while self.is_stopped():
            pass

        while self.is_running_forwards() and self.steps < self.lastStep:
            self.do_steps()
        self.clean_up()

    def get_sm(self):
        return self.sm

    def do_steps(self):
        if self.delay > 0.0005:
            self.delay = math.exp(-self.count) + 0.0005
            self.count = self.count + 0.02

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

        self.steps = self.steps + 1
        GPIO.output(STEP, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(self.delay)
        self.update_position()
        print(self.steps)

    def update_position(self):
        self.position[0] += 1
        self.position[1] += 1

    def set_steps(self, steps):
        self.lastStep = steps

    def set_steps_cm(self, distanceInMili):
        y = distanceInMili/float(10)
        steps = round(-100*(math.sqrt(-1000*(y - 2215.269))-1480), 0)
        self.lastStep = steps

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    @staticmethod
    def set_direction(direction):
        GPIO.output(DIR, direction)
    @staticmethod
    def clean_up():
        print("\nStepperH OFF")
        GPIO.cleanup()
