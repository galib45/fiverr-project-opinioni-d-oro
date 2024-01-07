import json
import random
import re
import secrets
from inspect import getframeinfo, stack
from string import ascii_uppercase, digits
from sys import stderr
from urllib.parse import urlencode, urlparse, urlunparse

import requests

from myapp import app

request_count = 0


def short_form(name):
    return "".join([word[0] for word in name.split() if word[0].isalpha()]).upper()


def generate_campaign_code(store_name, campaign_name):
    return f"{short_form(store_name)}{short_form(campaign_name)}"


def generate_random_code(length=8):
    return "".join(secrets.choice(ascii_uppercase + digits) for i in range(length))


def log_info(info):
    caller = stack()[1]
    filename = caller.filename.split("/")[-1]
    lineno = caller.lineno
    app.logger.info(f"[{filename}, line {lineno}] {info}\t")


def log_error(error):
    caller = stack()[1]
    filename = caller.filename.split("/")[-1]
    lineno = caller.lineno
    app.logger.error(f"[{filename}, line {lineno}] {error}", file=stderr)


def get_ua_list(filename):
    ua_list = []
    with open(filename, "r") as file:
        contents = file.read()
    ua_list.extend(filter(None, contents.split("\n")))
    return ua_list


ua_list = get_ua_list("useragents.txt")


def get_random_ua():
    global ua_list
    ua = random.choice(ua_list)
    log_info(f"User-Agent: {ua}")
    return ua


def requests_get(url, ua):
    global request_count
    headers = {"User-Agent": ua}
    reponse = None
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        log_error(e)
    request_count += 1
    return response


def get_id_from_url(share_url):
    ua = get_random_ua()
    response = requests_get(share_url, ua)

    pattern = r'"ChIJ[a-zA-Z0-9]+\\"'
    result = re.search(pattern, response.text)
    place_id = None
    if result:
        place_id = result.group()[1:-2]

    actual_url = response.url
    pattern = r"1s0x[0-9a-f]+:0x[0-9a-f]+"
    result = re.search(pattern, actual_url)
    unique_id = None
    if result:
        unique_id = result.group()[2:]

    return place_id, unique_id


def get_ua_id(share_url, ua):
    response = requests_get(share_url, ua)
    pattern = r"\"Bangladesh\"\],null,0,\".*?\""
    result = re.search(pattern, response.text)
    ua_id = None
    if result:
        ua_id = result.group()[22:-1]
    return ua_id


def build_pb(unique_id, page_id=""):
    pb = (
        "!1m7!1s"
        + unique_id
        + "!3s!6m4!4m1!1e1!4m1!1e3!2m2!1i10!2s"
        + page_id
        + "!3e2!5m2!1sHE9HZbeXBv-t4-EPjcSyuA0!7e81!8m5!1b1!2b1!3b1!5b1!7b1!11m6!1e3!2e1!3sen!4sbd!6m1!1i2"
    )
    return pb


def build_url(query_params):
    base_url = "https://www.google.com/maps/rpc/listugcposts"
    base_url_struct = urlparse(base_url)
    query_string = urlencode(query_params, safe="!")
    url = urlunparse(
        (
            base_url_struct.scheme,
            base_url_struct.netloc,
            base_url_struct.path,
            base_url_struct.params,
            query_string,
            base_url_struct.fragment,
        )
    )
    return url


def get_review_list(unique_id, upto_timestamp):
    page_id = ""
    query_params = {
        "authuser": "0",
        "hl": "en",
        "gl": "bd",
    }

    idx = 1
    review_list = []
    ua = get_random_ua()

    while True:
        query_params["pb"] = build_pb(unique_id, page_id)
        url = build_url(query_params)
        response = requests_get(url, ua)
        data = json.loads(response.text[5:])
        page_id = data[1]
        limit_reached = False
        for item in data[2]:
            account_slot = item[0][1]
            review_slot = item[0][2]

            name = account_slot[4][0][4]
            timestamp = account_slot[3] / 1000000
            if timestamp < upto_timestamp:
                limit_reached = True
                break
            account_id = account_slot[10]

            rating = review_slot[0][0]
            review = ""
            photos = []
            if len(review_slot) > 1:
                if review_slot[1] is not None:
                    review = review_slot[1][0]
                if review_slot[2] is not None:
                    photos = [photo[0] for photo in review_slot[2]]
            review_list.append([account_id, timestamp, rating, review, photos])
            idx += 1
        if page_id == None:
            break
        if limit_reached:
            break

    return review_list

def sendtext(addresses, message): 
    # The function that should be called from within the Flask app
    
    # Base URL for accessing the API
    API_BASE = 'https://api.pushbullet.com/v2'
    headers = {
        'Access-Token': app.config["PB_ACCESS_TOKEN"],
        'Content-Type': 'application/json'
    }

    # To send a text message, we need the device ID of the mobile phone connected to Pushbullet
    try:
        response = requests.get(API_BASE + '/devices', headers = headers)
        devices = json.loads(response.text)['devices']
    except requests.ConnectionError:
        print('Connection error. Please check your internet connection and try again.')
        return
                      
    device_id = None
    for device in devices:
        can_send_sms = device.get('has_sms') and device.get('active')
        if can_send_sms: 
            device_id = device.get('iden')
            break
    
    if not device_id:
        print("Device is inactive or sms has not been enabled yet. Check your device.")
        return
    
    data = {}
    data['addresses'] = addresses
    data['message'] = message
    data['target_device_iden'] = device_id

    try:
        resp = requests.post(API_BASE + '/texts', headers = headers, json = { 'data': data })
        return resp.status_code
        
    except requests.ConnectionError:
        print("Connection error. Please check your internet connection and try again.")
        return

# if __name__ == "__main__":
#     share_url = "https://maps.app.goo.gl/rTC36vzFQ4uKqZqC7"
#     _, unique_id = get_id_from_url(share_url)
#     review_list = get_review_list(share_url, unique_id)
#     print(request_count)
