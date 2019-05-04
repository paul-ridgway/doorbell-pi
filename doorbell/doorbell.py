from doorbell.OSCheck import ispi
from doorbell.mailgun import Mailgun
from doorbell.sms import Sms
from doorbell.config import Config
import logging
import time
from datetime import datetime
from dateutil import tz
import threading
import socket

UPSTAIRS_BELL_PIN = 20
DOWNSTAIRS_BELL_PIN = 21

if ispi():
    import RPi.GPIO as GPIO
else:
    from doorbell.EmulatorGUI import GPIO

L = logging.getLogger('Doorbell')


class Doorbell:

    def __init__(self):
        self.email = Mailgun()
        self.sms = Sms()
        self.config = Config()

        # TODO: Move to config?
        self.__email_recipients = ['paul@ridgway.io', 'amanda@ridgway.io']
        # self.__email_recipients = ['paul@ridgway.io', 'amanda@ridgway.io', 'stvrdgwy@gmail.com']
        self.__sms_recipients = ['+447507400113', '+447846709005']
        # self.__sms_recipients = ['+447507400113', '+447846709005', '+447905487269', '+447905822201']

        if not "doorbell" in socket.gethostname():
            L.info("Stubbing email/SMS contacts for non-prod host: %s", socket.gethostname())
            self.__email_recipients = ['paul@ridgway.io']
            self.__sms_recipients = ['+447507400113']

    def run(self):
        L.info("run")


        if not ispi():
            L.info("launching emulator")
            GPIO.init()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(UPSTAIRS_BELL_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(DOWNSTAIRS_BELL_PIN, GPIO.OUT, initial=GPIO.LOW)

        start = 0
        high = 0

        L.info("ready")

        while True:
            if GPIO.input(4) and high == 0:
                start = time.time()
                high = time.time()
                self.ding()

            if start > 0:
                if (time.time() - start) >= 1:
                    start = 0
                    self.dong()
            if not GPIO.input(4) and start == 0 and high > 0:
                if (time.time() - high) >= 5:
                    L.info("Cooled off, ready to fire again!")
                    high = 0
            time.sleep(0.05)

    def ding(self):
        L.info("Ding!")

        self.send_sms()
        self.send_email()

        if self.config.ring_upstairs:
            L.info("Ring Upstairs")
            GPIO.output(UPSTAIRS_BELL_PIN, GPIO.HIGH)
        else:
            L.info("Skipping Ring Upstairs due to config")

        if self.config.ring_downstairs:
            L.info("Ring Downstairs")
            GPIO.output(DOWNSTAIRS_BELL_PIN, GPIO.HIGH)
        else:
            L.info("Skipping Ring Downstairs due to config")

    def dong(self):
        L.info("Dong!")
        GPIO.output(UPSTAIRS_BELL_PIN, GPIO.LOW)
        GPIO.output(DOWNSTAIRS_BELL_PIN, GPIO.LOW)

    def send_email(self):
        # Email
        if self.config.send_email:
            L.info("Sending Email...")
            threading.Thread(target=self.notify_email, args=[self.__email_recipients]).start()
        else:
            L.info("Skipping E-Mail due to config")

    def send_sms(self):
        if self.config.send_sms:
            L.info("Sending SMS...")
            for number in self.__sms_recipients:
                threading.Thread(target=self.notify_sms, args=[number]).start()
        else:
            L.info("Skipping SMS due to config")

    def shutdown(self):
        L.info("shutdown")
        self.config.save()
        if not ispi():
            L.info("closing emulator")
            GPIO.shutdown()
        GPIO.cleanup()

    def notify_sms(self, sms_recipient):
        sender = '166'
        if not "doorbell" in socket.gethostname():
            sender = socket.gethostname()
        self.sms.send(sender, sms_recipient, "Doorbell @ " + self.local_time().strftime('%l:%M%p'))

    def notify_email(self, email_recipients):
        sender = "Doorbell"
        if not "doorbell" in socket.gethostname():
            sender = socket.gethostname()
        self.email.send(sender + " <doorbell@ridgway.io>", email_recipients,
                        "Doorbell @ " + self.local_time().strftime('%l:%M%p'),
                        "The doorbell rang at " + self.local_time().strftime('%l:%M%p %Z on %b %d, %Y'))
    def local_time(self):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/London')
        utc = datetime.utcnow()
        utc = utc.replace(tzinfo=from_zone)
        return utc.astimezone(to_zone)
