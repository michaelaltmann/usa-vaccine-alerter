from twilio.rest import Client
import requests
import threading
import datetime
import sys
import json
from twilio.base.exceptions import TwilioRestException
import signal


def clean_config(alert):
    if not alert['zip_codes']:
        alert['zip_codes'] = []
    if not alert['cities']:
        alert['cities'] = []
    alert['cities'] = [city.lower() for city in alert['cities']]
    return alert


# Twilio initialization
use_twilio = len(sys.argv[1:]) == 2
if use_twilio:
    account_sid = sys.argv[1]  # twilio account SID
    auth_token = sys.argv[2]  # twilio account auth token
    client = Client(account_sid, auth_token)


def check_appointments():
    global previous_messages
    try:
        data = requests.get(
            'https://www.vaccinespotter.org/api/v0/states/{state}.json'.format(state=config['state'])).json()
    except:
        print(
            f"Failed to fetch {config['state']} state data. Confirm this is a valid two letter state identifier and try again later.")
        return
    for alert in config["alerts"]:
        alert_name = alert["name"]
        features_with__appointments = filter_features(data, alert)

        messages = []
        for feature in features_with__appointments:
            for appointment in feature['properties']["appointments"]:
                message = compose_message(feature, appointment)
                messages.append(message)
        new_messages = [
            m for m in messages if m not in previous_messages.get(alert_name, [])]
        message = "\n".join(new_messages)
        if new_messages:
            if use_twilio:
                for number in alert['to']:
                    send_message(message,
                                 number, alert['from'])
            print(f"{time()} - New appointments found for {alert_name}!\n{message}")
        previous_messages[alert_name] = messages
        print(f"{time()} - No new appointments found for {alert_name}.")


def compose_message(feature, appointment):
    d = datetime.datetime.fromisoformat(appointment['time'])
    return f"{feature['properties']['provider_brand_name']} {feature['properties']['name']} in {feature['properties']['city']} at {d.strftime('%m/%d %H:%M')}"


def filter_features(data, alert):
    return [feature for feature in data['features'] if filter_feature(feature, alert)]


def filter_feature(f, alert):
    of_interest = (f['properties']['appointments_available'] and
                   (match_zipcode(f, alert) or
                    match_city(f, alert) or
                    match_box(f, alert)
                    )
                   )
    return of_interest


def match_zipcode(f, alert):
    return alert['zip_codes'] and f['properties']['postal_code'] in alert['zip_codes']


def match_city(f, alert):
    return alert['cities'] and f['properties']['city'].lower() in alert['cities']


def match_box(f, alert):
    lon = f['geometry']['coordinates'][0]
    lat = f['geometry']['coordinates'][1]
    box = alert['box']
    return box and lon >= box["min_lon"] and lon <= box["max_lon"] and lat >= box["min_lat"] and lat <= box["max_lat"]


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


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def terminate(a, b):
    print("Terminating")
    interval.cancel()


# load configuration data
try:
    file = open('config.json')
except IOError:
    print("config.json file not found.")
    exit(1)
config = json.load(file)
config["alerts"] = [clean_config(alert) for alert in config["alerts"]]

previous_messages = {}
signal.signal(signal.SIGINT, terminate)
signal.signal(signal.SIGQUIT, terminate)

# initial check
check_appointments()

# check every 60 seconds
interval = set_interval(check_appointments, 60)
