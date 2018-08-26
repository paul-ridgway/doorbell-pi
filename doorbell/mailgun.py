import requests
import logging
import yaml
import os


class Mailgun:

    def __init__(self):
        self.settings = None
        if os.path.exists('email.yml'):
            self.settings = yaml.safe_load(open('email.yml'))
            if 'mailgun_api_key' not in self.settings:
                raise KeyError("mailgun_api_key is missing from email.yml")
            if 'mailgun_domain_name' not in self.settings:
                raise KeyError("mailgun_domain_name is missing from email.yml")
            logging.info("Email enabled")

    def send(self, sender, to, subject, body, html_body=None):
        logging.info("Email#send, sender = %s, to = %s, subject = %s, body = %s", sender, to, subject, body)

        if self.settings is None:
            logging.warning("Skipping send as email settings (email.yml) are missing")
            return

        if html_body is None:
            html_body = body

        url = 'https://api.mailgun.net/v3/{}/messages'.format(self.settings['mailgun_domain_name'])
        auth = ('api', self.settings['mailgun_api_key'])
        data = {
            'from': sender,
            'to': to,
            'subject': subject,
            'text': body,
            'html': html_body
        }

        # files = [("attachment", open("example-attachment.txt"))]
        # response = requests.post(url, auth=auth, data=data, files=files)

        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()
        logging.info("Email#send - completed")
