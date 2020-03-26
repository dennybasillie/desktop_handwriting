import requests
import json

class GoogleIMERecognizer():

    URL = 'https://inputtools.google.com/request?itc=en-t-i0-handwrit&app=translate'
    
    def __init__(self, config):
        self.traces = []
        self.writing_area = { 'width': config['width'], 'height': config['height'] }
        self.language = config['language']

    def add_stroke(self, strokes, append = True):
        if append:
            self.traces.append(strokes)
        else:
            self.traces.extend(strokes)

    def detect(self):
        if len(self.traces) < 1:
            return None
            
        data = {
            'options': 'enable_pre_space',
            'requests': [{
                'writing_guide': {
                    'writing_area_width': self.writing_area['width'],
                    'writing_area_height': self.writing_area['height']
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

    def change_area(self, writing_area):
        self.writing_area = writing_area

    def clear(self):
        self.traces = []