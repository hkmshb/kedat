"""
Provides access to the Survey platforms data via API.
"""
import json
from urllib.parse import urlencode

import requests
import settings
from pprint import pprint


BASE_URL='http://survey.kedco.ng/api/v1/%s'
SURVEY_TEST_API_TOKEN='4b84e4ee77128d8e1d7801fb9bbf3e1c3954ed1e'
AUTH_HEADER = {'Authorization': 'Token ' + SURVEY_TEST_API_TOKEN }

FORM_CACHE = {}


def get_xform_info(name):
    r = requests.get(BASE_URL % 'data', headers=AUTH_HEADER)
    records = r.json()
    for record in records:
        if record['id_string'] == name:
            return [record]
    return []


def get_instances(name, start=None, start_date=None): 
    if name not in FORM_CACHE:
        form = get_xform_info(name)
        if form:
            FORM_CACHE[name] = form[0]
    
    form = FORM_CACHE.get(name)
    url = form['url']
    if start_date:
        url = "%s?query={\"datetime_today\":\"%s\"}" % (url, start_date)

    if start:
        url_fmt = "%s&start=%s" if start_date else "%s?start=%s"
        url = url_fmt % (url, start)

    print(url)
    r = requests.get(url, headers=AUTH_HEADER)
    return r.json()


def get_captures(activity):
    query = '{"datetime_today": "%s"}' % activity['sync_date']
    return _get_records(activity['sync_table'], query=query)


def _get_records(name, start=0, limit=100, query=None):
    def pull(form, start_at):
        params = urlencode({'start':start_at, 'limit':limit})
        if query:
            params += '&query=%s' % query

        url = "%s?%s" % (form['url'], params)
        r = requests.get(url, headers=AUTH_HEADER)
        return r.json()

    if name not in FORM_CACHE:
        form = get_xform_info(name)
        if form:
            FORM_CACHE[name] = form[0]

    form = FORM_CACHE.get(name)
    data = pull(form, start)
    yield data

    while (len(data) == limit):
        start += limit
        data = pull(form, start)
        yield data
