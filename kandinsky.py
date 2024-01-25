# _*_ coding: utf8 _*_

import base64
from io import BytesIO
import json
import time
import requests
from PIL import Image

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=30, delay=3):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)



def convert(base64_string, output_file='output.jpg'):
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    image.save(output_file, 'JPEG')
    return output_file

def img_generation(text):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '89069307908B573AB9634FA97F1E1724', '354830A9FE9798672E9283D9F0656565')
    model_id = api.get_model()
    uuid = api.generate(text, model_id)
    images = api.check_generation(uuid)[0]
    img = Image.open(convert(images))
    return img