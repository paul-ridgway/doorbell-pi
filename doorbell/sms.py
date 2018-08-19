import requests
import logging
import yaml
import os
from clx.xms import api, client, exceptions


class Sms:

    def __init__(self):
        self.settings = None
        if os.path.exists('sms.yml'):
            self.settings = yaml.safe_load(open('sms.yml'))
            if 'username' not in self.settings:
                raise KeyError("username is missing from sms.yml")
            if 'password' not in self.settings:
                raise KeyError("password is missing from sms.yml")
            logging.info("SMS enabled")

    def send(self, sender, recipient, body):
        logging.info("Sms#send, sender = %s, recipient = %s, body = %s", sender, recipient, body)

        if self.settings is None:
            logging.warning("Skipping send as email settings (sms.yml) are missing")
            return

        c = client.Client(self.settings['username'], self.settings['password'])
        c.create_text_message(
            sender=sender,
            recipient=recipient,
            body=body)
        logging.info("Sms#send - completed")
