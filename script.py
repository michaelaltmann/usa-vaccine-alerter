from twilio.rest import Client
import requests
import threading
import datetime
import sys
import json
from twilio.base.exceptions import TwilioRestException
import signal

# load configuration data
try:
    file = open('config.json')
except IOError:
    print("config.json file not found.")
    exit(1)
config = json.load(file)


# Twilio initialization
use_twilio = len(sys.argv[1:]) == 2
if use_twilio:
    account_sid = sys.argv[1]  # twilio account SID
    auth_token = sys.argv[2]  # twilio account auth token
    client = Client(account_sid, auth_token)


def check_appointments():
    try:
        data = requests.get(
            'https://www.vaccinespotter.org/api/v0/states/{state}.json'.format(state=config['state'])).json()
    except:
        print(
            f"Failed to fetch {config['state']} state data. Confirm this is a valid two letter state identifier and try again later.")
        return
    appointment = find_appointment(data)
    if (appointment != None):
        message = compose_message(appointment)
        if use_twilio:
            for number in config['to']:
                send_message(message,
                             number, config['from'])
        print(f"{time()} - Appointment found!\n\n{message}")
        exit(0)
    print(f"{time()} - No appointments found. ")


def compose_message(appointment):
    return f"COVID-19 vaccine located! {appointment['properties']['provider_brand_name']} in {appointment['properties']['city']}, {appointment['properties']['state']}. Book ASAP:\n\n{appointment['properties']['url']}"


def find_appointment(data):
    for feature in data['features']:
        if ((feature['properties']['postal_code'] in config['zip_codes'] or
                feature['properties']['city'].lower() in list_to_lower(config['cities'])) and feature['properties']['appointments_available']):
            return feature
    return None


def send_message(message, to, from_):
    try:
        message = client.messages.create(
            body=message, to=to, from_=from_)
        print(f"Text message sent to {to}!")
        return message.sid
    except TwilioRestException as e:
        print("Failed to send text message.")
        print(e.msg)


def time():
    return str(datetime.datetime.now())


def list_to_lower(uppercase_list: list):
    return [i.lower() for i in uppercase_list]


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def terminate(a, b):
    interval.cancel()

signal.signal(signal.SIGINT, terminate)
# initial check
check_appointments()

# check every 60 seconds
interval = set_interval(check_appointments, 60)
