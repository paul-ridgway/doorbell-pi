from doorbell.OSCheck import ispi
from doorbell.email import Email
import logging
import time
import threading
import socket

if ispi():
    import RPi.GPIO as GPIO
else:
    from doorbell.EmulatorGUI import GPIO

L = logging.getLogger('Doorbell')


class Doorbell:

    def __init__(self):
        self.email = Email()

    def run(self):
        L.info("run")

        recipients = ['paul@ridgway.io', 'amanda@ridgway.io']

        if not ispi():
            L.info("launching emulator")
            GPIO.init()
            recipients = ['paul@ridgway.io']

        if not "doorbell" in socket.gethostname():
            L.info("Stubbing email contacts for non-prod host: %s", socket.gethostname())
            recipients = ['paul@ridgway.io']

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

        high = False

        # GPIO.add_event_detect(4, GPIO.BOTH)
        L.info("ready")

        while True:
            if GPIO.input(4) and not high:
                L.info("Ding!")
                GPIO.output(14, GPIO.HIGH)
                GPIO.output(15, GPIO.HIGH)
                threading.Thread(target=self.notify, args=recipients).start()
                high = True
            elif (not GPIO.input(4)) and high:
                if high:
                    L.info("Dong!")
                    GPIO.output(14, GPIO.LOW)
                    GPIO.output(15, GPIO.LOW)
                    high = False
            time.sleep(0.05)

    def shutdown(self):
        L.info("shutdown")
        if not ispi():
            L.info("closing emulator")
            GPIO.shutdown()
        GPIO.cleanup()

    def notify(self, recipients):
        sender = "Doorbell"
        if not "doorbell" in socket.gethostname():
            sender = socket.gethostname()
        self.email.send(sender + " <doorbell@ridgway.io>", recipients,
                     "Doorbell @ " + time.strftime('%l:%M%p'),
                     "The doorbell rang at " + time.strftime('%l:%M%p %Z on %b %d, %Y'))
