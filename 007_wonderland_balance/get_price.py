import requests
from pprint import pprint

from dotenv import load_dotenv
import os
# import nomics API key from .env
load_dotenv()
NOMICS_API_KEY = os.getenv('NOMICS_API_KEY')

def get_token_price(token_id):
    url = 'https://api.nomics.com/v1/currencies/ticker'
    payload = {
        'key': NOMICS_API_KEY,
        'ids': token_id
    }
    response = requests.get(url, params=payload)
    return response.json()[0]['price']

print(type(get_token_price(token_id='TIME5')))
