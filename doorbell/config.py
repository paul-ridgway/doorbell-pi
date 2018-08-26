import os
import yaml
import logging

L = logging.getLogger('Config')


class Config:

    def __init__(self):
        # Defaults
        self.__send_sms = True
        self.__send_email = True
        self.__ring_upstairs = True
        self.__ring_downstairs = True
        self.load()

    @property
    def send_sms(self):
        return self.__send_sms

    @property
    def send_email(self):
        return self.__send_email

    @property
    def ring_upstairs(self):
        return self.__ring_upstairs

    @property
    def ring_downstairs(self):
        return self.__ring_downstairs

    def load(self):
        L.info("Loading")
        if os.path.isfile("config.yml"):
            stream = open("config.yml", "r")
            doc = yaml.load(stream)
        else:
            L.info("config.yml does not exist, using defaults")
            doc = dict()

        # Load properties
        self.__send_sms = doc.get("send_sms", self.__send_sms)
        self.__send_email = doc.get("send_email", self.__send_email)
        self.__ring_upstairs = doc.get("ring_upstairs", self.__ring_upstairs)
        self.__ring_downstairs = doc.get("ring_downstairs", self.__ring_downstairs)

    def save(self):
        L.info("Saving")
        data = dict(
            send_sms=self.__send_sms,
            send_email=self.__send_email,
            ring_upstairs=self.__ring_upstairs,
            ring_downstairs=self.__ring_downstairs
        )
        with open('config.yml', 'w') as outfile:
            outfile.write(yaml.dump(data))
