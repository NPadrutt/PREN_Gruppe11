import multiprocessing

import RPi.GPIO as GPIO
import time
from StateMachine import StateMachine

GPIO_ECHO = 18


class CollisionButton(multiprocessing.Process):
    _states = ['initialized', 'running', 'stopped']

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)

        self.task_queue = task_queue
        self.result_queue = result_queue
        self.is_running = True

        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        # set GPIO Pins

        # set GPIO input (IN / OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        self.sm = StateMachine.get_collision_machine(self, CollisionButton._states)
        print("[ CollisionButton ] Initialized")

    def run(self):
        while self.is_running:
            time.sleep(1.5)
            # print("[ CollisionButton ]" + str(GPIO.input(GPIO_ECHO)))
            if GPIO.input(GPIO_ECHO):
                print("[ CollisionButton ] Collided")
                self.result_queue.put(True)
                self.is_running = False

    def get_sm(self):
        return self.sm
