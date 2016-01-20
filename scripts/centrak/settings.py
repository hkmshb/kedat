"""
Application wide settings.
"""
import os
import sys


# directory paths
BASE_DIR = os.path.dirname(__file__)
KEDAT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
sys.path.append(KEDAT_DIR)


# API
API_BASE_URL='http://survey.kedco.ng/api/v1/%s'

API_TOKEN_SURVEY_TEST='4b84e4ee77128d8e1d7801fb9bbf3e1c3954ed1e'
API_TOKEN_EAGLE_EYE='12a13a30fb3d3016826240840649d9b966abc4f6'
API_DEFAULT_TOKEN=API_TOKEN_EAGLE_EYE

AUTH_HEADER = {
    'Authorization': 'Token ' + API_DEFAULT_TOKEN 
}


# pagination
PAGE_SIZE = 20

# formats
FMT_SHORTDATE = '%Y-%m-%d'

