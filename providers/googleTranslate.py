import requests
import json

class GoogleTranslate():

    URL = 'https://translate.googleapis.com/translate_a/single?client=gtx&dt=t'
    
    def __init__(self, config):
        self.languages = { 'source': config['source'], 'target': config['target'] }

    def translate(self, query):
        encoded_query = requests.utils.quote(query)
        full_url = self.URL + f"&sl={self.languages['source']}&tl={self.languages['target']}&q={encoded_query}"
        response = requests.get(full_url)
        #TODO: check response.status_code and process response.text[0]
        candidates = json.loads(response.text)[0][0][0]
        return candidates

    def change_language(self, language):
        self.languages = language

    def set_autodetect(self):
        self.languages['source'] = 'auto'