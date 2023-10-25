import requests
from urllib.parse import urlparse, urlencode, urlunparse
import json
import re
import random

request_count = 0

def get_ua_list(filename):
    ua_list = []
    with open(filename, 'r') as file:
        contents = file.read()
    ua_list.extend(filter(None, contents.split('\n')))
    return ua_list

ua_list = get_ua_list('useragents.txt')

def get_random_ua():
    global ua_list
    ua = random.choice(ua_list)
    print('User-Agent:', ua)
    return ua

ua = get_random_ua()

def requests_get(url):
    global ua
    global request_count
    headers = {
        'User-Agent': ua
    }
    reponse = None
    try: response = requests.get(url, headers=headers)
    except Exception as e: print(e)
    request_count += 1
    if request_count % 10 == 0: ua = get_random_ua()
    return response

def get_unique_id(share_url):
    response = requests_get(share_url)
    actual_url = response.url
    pattern = r'1s0x[0-9a-f]+:0x[0-9a-f]+'
    result = re.search(pattern, actual_url)
    unique_id = None
    if result != None: unique_id = result.group()
    return unique_id

def build_pb(unique_id, page_id=''):
    pb = '!1m7!' + unique_id + '!3s!6m4!4m1!1e1!4m1!1e3!2m2!1i10!2s' + page_id + '!3e2!5m2!1sobw0ZajDMcOcseMP2oSm2A0!7e81!8m5!1b1!2b1!3b1!5b1!7b1!11m6!1e3!2e1!3sen!4sbd!6m1!1i2'
    return pb

def build_url(query_params):
    base_url = 'https://www.google.com/maps/rpc/listugcposts'
    base_url_struct = urlparse(base_url)
    query_string = urlencode(query_params, safe='!')
    url = urlunparse((
        base_url_struct.scheme, base_url_struct.netloc,
        base_url_struct.path, base_url_struct.params,
        query_string, base_url_struct.fragment
    ))
    return url

def get_review_list(unique_id):
    page_id = ''
    query_params = {
        'authuser': '0',
        'hl': 'en',
        'gl': 'bd',
    }

    idx = 1
    review_list = []

    while True:
        query_params['pb'] = build_pb(unique_id, page_id)
        url = build_url(query_params)
        response = requests_get(url)
        data = json.loads(response.text[5:])
        page_id = data[1]
        for item in data[2]:
            name = item[0][1][4][0][4]
            time = item[0][1][6]
            review_slot = item[0][2]
            review = ''
            if len(review_slot) > 1: 
                if review_slot[1] != None: review = review_slot[1][0]
            if __name__ == '__main__': print(idx, name + ', ' + time + ', ' + review.replace('\n', ' '))
            review_list.append([name, time, review])
            idx += 1
        if page_id==None: break

    return review_list

if __name__ == '__main__':
    share_url = 'https://maps.app.goo.gl/QgLtXEWHt5m9ZbAt8'
    unique_id = get_unique_id(share_url)
    review_list = get_review_list(unique_id)
    print(request_count)
