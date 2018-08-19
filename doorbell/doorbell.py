from doorbell.OSCheck import ispi
from doorbell.email import Email
from doorbell.sms import Sms
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
        self.sms = Sms()

    def run(self):
        L.info("run")

        email_recipients = ['paul@ridgway.io', 'amanda@ridgway.io']
        sms_recipients = ['+447507400113', '+447846709005']

        if not ispi():
            L.info("launching emulator")
            GPIO.init()

        if not "doorbell" in socket.gethostname():
            L.info("Stubbing email/SMS contacts for non-prod host: %s", socket.gethostname())
            email_recipients = ['paul@ridgway.io']
            sms_recipients = ['+447507400113']
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

        start = 0
        high = 0

        # GPIO.add_event_detect(4, GPIO.BOTH)
        L.info("ready")

        while True:
            if GPIO.input(4) and high == 0:
                L.info("Ding!")
                start = time.time()
                high = time.time()
                GPIO.output(14, GPIO.HIGH)
                GPIO.output(15, GPIO.HIGH)
                threading.Thread(target=self.notify_email, args=[email_recipients]).start()
                for number in sms_recipients:
                    threading.Thread(target=self.notify_sms, args=[number]).start()
            if start > 0:
                if (time.time() - start) >= 1:
                    L.info("Dong!")
                    GPIO.output(14, GPIO.LOW)
                    GPIO.output(15, GPIO.LOW)
                    start = 0
            if not GPIO.input(4) and start == 0 and high > 0:
                if (time.time() - high) >= 5:
                    L.info("Cooled off, ready to fire again!")
                    high = 0
            time.sleep(0.05)

    def shutdown(self):
        L.info("shutdown")
        if not ispi():
            L.info("closing emulator")
            GPIO.shutdown()
        GPIO.cleanup()

    def notify_sms(self, sms_recipient):
        sender = 'Doorbell'
        if not "doorbell" in socket.gethostname():
            sender = socket.gethostname()
        self.sms.send(sender, sms_recipient, "Doorbell @ " + time.strftime('%l:%M%p'))

    def notify_email(self, email_recipients):
        sender = "Doorbell"
        if not "doorbell" in socket.gethostname():
            sender = socket.gethostname()
        self.email.send(sender + " <doorbell@ridgway.io>", email_recipients,
                        "Doorbell @ " + time.strftime('%l:%M%p'),
                        "The doorbell rang at " + time.strftime('%l:%M%p %Z on %b %d, %Y'))
