"""
Routes for API access.
"""
from bottle import route, request
from services import api



@route('/api/survey/captures')
def captures():
    action = request.forms.get('action')
    form_id = request.forms.get('form_id')
    date_capture = request.forms.get('date_capture')
    

    
