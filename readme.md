# USA Vaccine Availability Alerter Script

This script uses the API provided by [covid-vaccine-spotter](https://github.com/GUI/covid-vaccine-spotter) to send a text message when a vaccine has been located.

## Setup

### Using Twilio

1. Install requirements by running `pip install -r requirements.txt`
2. Setup a Twilio account. Free trial link: [(refferal)](www.twilio.com/referral/WTOydE) [(no refferal)](https://www.twilio.com/try-twilio)
   - Get a phone number
   - Note your phone number, SID, and Auth Token
3. Open `script.py`
4. In the config dictionary, customize the values to setup your search parameters.

```python
config = {
          'state': 'IA',  # two letter identifier (AL, AK, etc)
          'cities': ['Ames'],  # name of cities to monitor
          'zip_codes': ['50012'],  # zip codes to monitor
          'to': '+15555555555', # phone number to send to
          'from': '+15555555555' # phone number to send from,
        }
```

4. Save the updated file.
5. Call the program using `python3 script.py SID AUTH_TOKEN` where SID and AUTH_TOKEN are replaced with your proper tokens from twilio.

### Not Using Twilio (output printed to CLI)

1. Install requirements by running `pip install -r requirements.txt`
2. Open `script.py`
3. In the config dictionary, customize the values to setup your search parameters. Note that `to` and `from` are not needed.

```python
config = { 'state': 'IA',  # two letter identifier (AL, AK, etc)
          'cities': ['Ames'],  # name of cities to monitor
          'zip_codes': ['50012'],  # zip codes to monitor
        }
```

3. Save the updated file.
4. Call the program using `python3 script.py`

## MLH

Created for Major League Hacks: Share challenge, day 3.
