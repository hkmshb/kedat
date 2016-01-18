"""
Routes and views for the bottle application.
"""
from datetime import datetime
from bottle import (
    post, route, request, response, redirect, template,
    view as fn_view)

import db                
from utils import get_session, write_log
from settings import FMT_SHORTDATE
from services import api




def view(tmpl_name):
    context = {
        'year': datetime.now().year,
        'get_session': get_session,
        'request': request,
    }
    return fn_view(tmpl_name, **context)


@route('/')
@view('index')
def index():
    return {
        'is_front': True, 
        'title': 'Capture Summary',
    }


@route('/xforms/')
@view('xforms')
def xforms():
    forms = db.XForm.get_all()
    return {
        'year': datetime.now().year,
        'title': 'XForms',
        'records': forms
    }      


@post('/xforms/')
def xforms_sync():
    if 'sync' in request.forms:
        forms = api.get_xforms()
        failed, reports = [], []

        for f in forms:
            exist = db.XForm.get_by_id(f['id'])
            if exist: 
                continue
        
            try:
                f['date_created'] = datetime.now().strftime(FMT_SHORTDATE)
                db.XForm.insert_one(f)
            except Exception as ex:
                failed.append(f)
                reports.append(str(ex))

        session = get_session()
        messages = session['messages']
        if not failed:
            messages['pass'].append('Sync was successful.')
        else:
            all_failed = (len(forms) - len(failed)) == 0
            if all_failed:
                messages['fail'].append('Sync was unsuccessful.')
            else:
                msg = 'Sync was partially successful. %s entries failed.'
                messages['warn'].append(msg % len(failed))

            write_log(reports)

        session.save()
        return redirect('/xforms/')

    elif 'save' in request.forms:
        active = request.forms.getall('activate')
        startup_all = request.forms.get('startup-all').split(',')
        startup_active = request.forms.get('startup-active').split(',')

        updated = []

        # handle recently activated forms
        new_actives = [x for x in active if x not in startup_active]
        for id in new_actives:
            db.XForm.set_active(id, True)
            updated.append(id)

        # handle recently deactivated forms
        inactives = [x for x in startup_all if x not in active]
        startup_inactives = [x for x in startup_all if x not in startup_active]
        new_inactives = [x for x in inactives if x not in startup_inactives]
        for id in new_inactives:
            print(db.XForm.set_active(id, False))
            updated.append(id)

        if updated:
            session = get_session()
            session['messages']['pass'].append('%s XForm(s) Updated.' % len(updated))
            session.save()
        return redirect('/xforms/')




    



