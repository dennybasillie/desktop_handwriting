import requests
import json

class GoogleTranslate():
    #dt=t :: Top; dt=bd :: Alternatives; dt=rm :: Pinyin;
    URL = 'https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&dt=bd'
    
    def __init__(self, config):
        self.languages = { 'source': config['source'], 'target': config['target'] }

    def translate(self, query):
        encoded_query = requests.utils.quote(query)
        full_url = self.URL + f"&sl={self.languages['source']}&tl={self.languages['target']}&q={encoded_query}"
        response = requests.get(full_url)
        json_response = json.loads(response.text)

        candidates = []
        if json_response[1] is not None:
            candidates = json_response[1][0][1]
        
        top_candidate = json_response[0][0][0]
        if top_candidate not in candidates:
            candidates.insert(0,top_candidate)
        
        return candidates

    def change_language(self, language):
        self.languages = language

    def set_autodetect(self):
        self.languages['source'] = 'auto'