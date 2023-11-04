import json
import requests
import sys

# Placeholder values for some variables that will retrieve their values from the Flask application
file_token = 'pbtoken.txt'
file_contact = 'contacts.txt'
file_msgtemp = 'messagetemplate.txt'

# The function that should be called from within the Flask app
def sendtext(file_token, file_contact, file_msgtemp):
    # Reading necessary files
    with open(file_token, 'r') as f:
        PB_TOKEN = f.read().strip()
    with open(file_contact, 'r') as f:
        CONTACTS = [num.strip().split('::') for num in f.readlines()]
    with open(file_msgtemp, 'r') as f:
        msg_temp = f.read().strip()

    # Base URL for accessing the API
    API_BASE = 'https://api.pushbullet.com/v2'

    # To send a text message, we need the device ID of the mobile phone connected to Pushbullet
    try:
        devs = json.loads(requests.get(API_BASE + '/devices',\
                      headers = {'Access-Token': PB_TOKEN}).text)['devices']
    except requests.ConnectionError:
        print('Connection error. Please check your internet connection and try again.')
        return 0
                      
    for dev in devs:
        if (dev['has_sms'] if 'has_sms' in dev else 0) and dev['active']:
            DEV_ID = dev['iden']

    # Sending the message
    respdata = []
    for contact in CONTACTS:
        reqdata = {'data': 
                    {'addresses': [contact[1]],
                     'message': msg_temp.format(contact[0]),
                     'target_device_iden': DEV_ID}}
        try:
            resp = requests.post(API_BASE + '/texts', \
                                 headers = {'Access-Token': PB_TOKEN, \
                                 'Content-Type': 'application/json'},
                                 json = reqdata)
            respdata.append([resp.status_code, resp.text])
            if resp.status_code != 200:
                print(resp.error)
                return 0
        except requests.ConnectionError:
            print("Connection error. Please check your internet connection and try again.")
            return 0

    return respdata
