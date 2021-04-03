# USA Vaccine Availability Alerter Script

This script uses the API provided by [covid-vaccine-spotter](https://github.com/GUI/covid-vaccine-spotter) to send a text message when a vaccine has been located.

## Setup

### Using Twilio

1. Install requirements by running `pip install -r requirements.txt`
2. Setup a Twilio account. Free trial link: [(refferal)](www.twilio.com/referral/WTOydE) [(no refferal)](https://www.twilio.com/try-twilio)
   - Get a phone number
   - Note your phone number, SID, and Auth Token
3. Create a file named `config.json` and copy the below configuration code. Each phone number to send a message to should be listed in the "to" list.

```json
{
  "state": "MN",
  "alerts": [
    {
      "name": "Michael Altmann",
      "cities": [],
      "zip_codes": [],
      "box": {
        "min_lon": -95,
        "min_lat": 43.78,
        "max_lon": -92.45,
        "max_lat": 46
      },
      "from": "6125551212",
      "to": ["6125551212"]
    }
  ]
}
```

4. Edit the values to setup your search parameters and phone number details.
5. Save the updated file.
6. Call the program using `python3 script.py SID AUTH_TOKEN` where SID and AUTH_TOKEN are replaced with your proper tokens from twilio.

### Not Using Twilio (output printed to CLI)

1. Install requirements by running `pip install -r requirements.txt`
2. Create a file named `config.json` and copy the below configuration code.

```json
{ "state": "IL", "alerts": [{ "cities": ["Chicago"], "zip_codes": [] }] }
```

4. Edit the values to setup your search parameters.
5. Save the updated file.
6. Call the program using `python3 script.py`

## MLH

Created for Major League Hacks: Share challenge, day 3.
