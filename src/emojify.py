import requests
import json

URL = 'https://api.emojify.net/convert'

def emojify(text, density=50):
    payload = {
        'density' : density,
        'input' : text,
        'shouldFilterEmojis' : False
        }
    resp = requests.post(URL, json=payload)
    return json.loads(resp.text)['result'].replace(u'\u200b', '')