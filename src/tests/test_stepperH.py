from src.StepperH import StepperH


# starts horizontal stepper as thread
if __name__ == '__main__':
    stepper = StepperH()
    try:
        stepper.start()
        while True:
            print('stepper running')
    except(KeyboardInterrupt, SystemExit):
        stepper.running = False
        stepper.join()