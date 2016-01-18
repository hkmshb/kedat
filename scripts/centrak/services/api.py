"""
Provides access to the Survey platforms data via API.
"""
import json
from urllib.parse import urlencode

import requests
#import settings


BASE_URL = 'http://survey.kedco.ng/api/v1/%s'
SURVEY_TEST_API_TOKEN='4b84e4ee77128d8e1d7801fb9bbf3e1c3954ed1e'
AUTH_HEADER = {'Authorization': 'Token ' + SURVEY_TEST_API_TOKEN }

FORM_CACHE = {}



def get_xforms():
    r = requests.get(BASE_URL % 'data', headers=AUTH_HEADER)
    return r.json()



if __name__ == '__main__':
    from pprint import pprint
    pprint(get_xforms())

