"""
Routes for API access.
"""
from datetime import datetime
from bottle import route, request
from kedat.core import Storage as _
import db, forms


_CHOICES_CACHE = None



@route('/api/<record_type:re:(captures|updates)>/<record_id:int>/')
def captures(record_type, record_id):
    table = db.Capture if record_type == 'captures' else db.Update
    record = table.get(record_id)
    
    # del record['snapshots']         # exclude snapshots
    result = {'capture': record}
    if not request.query.get('record_only', False):
        result.update({
            '_choices': _collect_choices(),
            '_meta': forms.CaptureForm._meta
        })
    return result


@route('/api/<record_type:re:(captures|updates)>/<record_id:int>/update', method=['POST'])
def capture_update(record_type, record_id):
    table = db.Capture if record_type == 'captures' else db.Update
    record = table.get(record_id)
    if not record:
        return {'success':False, 'message':'Original record not found' }
    
    if not request.json:
        return {'success':False, 'message':'Posted record not available'}
    
    capture, snapshot = _(request.json['capture']), None
    if not record.snapshots:
        snapshot = record.copy()
        del snapshot['snapshots']
    else:
        snapshot = record['snapshots']['original']['capture']
        
    # save changes
    last_updated = datetime.today().strftime('%Y-%m-%d')
    capture.last_updated = last_updated
    capture.snapshots = {
        'original': {
            'capture': snapshot,
            'last_updated': last_updated,
            'updated_by': None
        }
    }
    table.replace(record_id, capture)
    return {'success':True, 'message':'Record updated!'}


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
