"""
Routes for API access.
"""
from bottle import route, request
import db, forms


_CHOICES_CACHE = None



@route('/api/<record_type:re:(captures|updates)>/<record_id:int>/')
def captures(record_type, record_id):
    table = db.Capture if record_type == 'captures' else db.Update
    record = table.get(record_id)
    
    result = {'capture': record}
    if not request.query.get('record_only', False):
        result.update({
            '_choices': _collect_choices(),
            '_meta': forms.CaptureForm._meta
        })
    return result


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
