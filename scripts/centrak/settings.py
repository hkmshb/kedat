"""
Application wide settings.
"""

API_BASE_URL='http://survey.kedco.ng/api/v1/%s'
API_DEFAULT_TOKEN='4b84e4ee77128d8e1d7801fb9bbf3e1c3954ed1e'


API_TOKEN = API_DEFAULT_TOKEN
AUTH_HEADER = {
    'Authorization': 'Token ' + API_TOKEN 
}


# pagination
PAGE_SIZE = 20
