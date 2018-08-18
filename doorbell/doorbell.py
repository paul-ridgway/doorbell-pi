from doorbell.OSCheck import ispi
import time

if ispi():
    import RPi.GPIO as GPIO
else:
    from doorbell.EmulatorGUI import GPIO


class Doorbell:

    def run(self):
        print("hello!")
        print(ispi())

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

        high = False

        try:
          # GPIO.add_event_detect(4, GPIO.BOTH)
          print("Ready")

          while True:
            if GPIO.input(4):
              print("Ding! ")
              GPIO.output(14, GPIO.HIGH)
              GPIO.output(15, GPIO.HIGH)
              high = True
            else:
              if high:
                print   ("Dong! ")
                GPIO.output(14, GPIO.LOW)
                GPIO.output(15, GPIO.LOW)
                high = False
            time.sleep(0.1)

        except KeyboardInterrupt:
          GPIO.cleanup()       # clean up GPIO on CTRL+C exit

        GPIO.cleanup()           # clean up GPIO on normal exit
