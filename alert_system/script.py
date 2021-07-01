
# libs for logging
import logging.config
import logging
# Init logger
logging.config.fileConfig('config/logger.conf')
logger = logging.getLogger(__name__)

import os
import json
import requests
import pyjokes
from iklubscrapper import get_new_articles

# libs for email
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# libs for twilio
from twilio.rest import Client

# Change directory to script dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))


with open("config/config.json", "r") as config_file:
    config = json.load(config_file)


script_dir = os.path.dirname(__file__)


def gen_cat_fact():
    url = "https://cat-fact.herokuapp.com/facts/random"
    data = requests.get(url).json()
    return data['text']


def gen_python_joke():
    return pyjokes.get_joke(language="en", category="neutral")


def send_sms(message_text, number):
    account_sid = config['twilio']['account_sid']
    auth_token = config['twilio']['account_sid']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=("Hello. " + message_text),
        to=number, # i.e. +421 043 325 583
        from_=config['twilio']['number']
    )

    print(message.sid)


def send_mail(receiver_email, subject, content, urls):


    port = 465  # SSL port
    sender_email = config['mail']['login']
    password = config['mail']['password']
    # This will load the system’s trusted CA certificates, enable host
    # name checking and certificate validation, and try to choose 
    # reasonably secure protocol and cipher settings.
    context = ssl.create_default_context()

    message = MIMEMultipart()
    # message = MIMEText(content, text_subtype)
    message['From'] = config['mail']['display_name']
    message['Subject'] = subject

    plainpart = MIMEText(content, 'plain')

    html = ""
    if urls:
        html += """
            <html>
            <head></head>
            <body>
            """

        for key, value in urls.items():
            html += f"<a href=\"{value}\">{key}</a>\n<br>\n"

        html += """
            </body>
            </html>
            """

    htmlpart = MIMEText(html, 'html')
    message.attach(plainpart)
    message.attach(htmlpart)

    # makes sure that the connection is automatically closed at the end of the "with" code
    with smtplib.SMTP_SSL(config['mail']['server'], port, context=context) as server:
        server.login(config['mail']['login'], password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def get_receivers():
    with open('config/subscribers.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        return lines


def send_new_alerts():
    new_articles = get_new_articles()

    if new_articles:
        for article in new_articles:
            content = article.subtitle + '\n' + article.text + '\n'
            for receiver in get_receivers():
                send_mail(receiver, article.title, content, article.urls)
                logger.info(f"Sending article to {receiver}, article title: {article.title}")
        logger.info(f"Successfully sent {len(new_articles)} article/s to {len(get_receivers())} receiver/s")


# def run():
#     while True:
#         message = gen_python_joke()
#         print(message)
#         if input("Sent this joke? y/n") == 'y':
#             send_sms(message, '949762450')
#             break

send_new_alerts()
