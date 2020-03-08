import requests
import json

class GoogleIMERecognizer():

    URL = 'https://www.google.com.tw/inputtools/request?ime=handwriting&app=mobilesearch&cs=1&oe=UTF-8'

    def __init__(self, config):
        self.traces = []
        self.writing_area = [config['width'], config['height']]
        self.language = config['language']

    def add_stroke(self, strokes):
        self.traces.append(strokes)

    def detect(self):
        data = {
            'options': 'enable_pre_space',
            'requests': [{
                'writing_guide': {
                    'writing_area_width': self.writing_area[0],
                    'writing_area_height': self.writing_area[1]
                },
                'ink': self.traces,
                'language': self.language
            }]
        }
        response = requests.post(self.URL, json=data)
        #TODO: check response.status_code and response.text[0]
        candidates = json.loads(response.text)[1][0][1]
        self.clear()
        return candidates

    def change_language(self, language):
        self.language = language

    def change_size(self, writing_area):
        self.writing_area = writing_area

    def clear(self):
        self.traces = []