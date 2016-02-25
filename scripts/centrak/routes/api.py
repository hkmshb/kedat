"""
Routes for API access.
"""
from bottle import route, request
import db, forms


_CHOICES_CACHE = None



@route('/api/captures/<capture_id:int>/')
def captures(capture_id):
    record = db.Capture.get(capture_id)
    return {
        'capture': record,
        '_choices': _collect_choices(),
        '_meta': forms.CaptureForm._meta
    }



def _collect_choices():
    global _CHOICES_CACHE 
    if not _CHOICES_CACHE:
        from collections import OrderedDict
        from services import choices
        
        all = {
            'acct_status': OrderedDict(choices.ACCT_STATUS),
            'tariff': OrderedDict(choices.TARIFF),
            'tariff_new': OrderedDict(choices.TARIFF_NEW),
            'meter_type': OrderedDict(choices.METER_TYPE),
            'meter_brand': OrderedDict(choices.METER_BRAND),
            'meter_phase': OrderedDict(choices.METER_PHASE),
            'meter_status': OrderedDict(choices.METER_STATUS),
            'meter_location': OrderedDict(choices.METER_LOCATION),
            'plot_type': OrderedDict(choices.PLOT_TYPE),
            'supply_source': OrderedDict(choices.SUPPLY_SOURCE),
            'occupant': OrderedDict(choices.OCCUPANT),
            'addy_state': OrderedDict(choices.ADDY_STATE),
        }
        _CHOICES_CACHE = all
    return _CHOICES_CACHE
