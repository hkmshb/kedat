"""
Provides access to the Survey platforms data via API.
"""
import json
from urllib.parse import urlencode

import requests
from settings import API_BASE_URL, AUTH_HEADER



FORM_CACHE = {}


def get_xforms():
    r = requests.get(API_BASE_URL % 'data', headers=AUTH_HEADER)
    return r.json()



if __name__ == '__main__':
    from pprint import pprint
    pprint(get_xforms())

