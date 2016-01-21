"""
Routes and views for the bottle application.
"""
from datetime import datetime, date
from bottle import (
    post, route, request, response, redirect, template,
    view as fn_view)
from kedat.core import Storage as _

import db                
from utils import get_session, write_log, get_weekdate_bounds
from settings import FMT_SHORTDATE
from services import api, stats



def view(tmpl_name):
    ref_date = _get_ref_date()
    wkdate_bounds = get_weekdate_bounds(ref_date)

    context = {
        'year': datetime.now().year,
        'get_session': get_session,
        'request': request,
        
        # calendar entries
        'ref_date': ref_date,
        'weekdate_bounds': wkdate_bounds,
    }
    return fn_view(tmpl_name, **context)


def _get_ref_date():
    try:
        ref_date = request.query.get('refdate', None)
        ref_date = (datetime.strptime(ref_date, '%Y%m%d').date()
                    if ref_date else datetime.today().date())
    except:
        ref_date = datetime.today().date()
    return ref_date


@route('/')
@view('index')
def index():
    #+==========================
    #: forms series summary
    records = []
    forms = db.XForm.get_all()
    ref_date = _get_ref_date()
    wkdate_bounds = get_weekdate_bounds(ref_date)

    for f in forms:
        record = _(id_string=f.id_string, title=f.title)
        captures = db.Capture.get_by_form(f.id_string, paginate=False)
        if captures.count():
            summary = stats.series_purity_summary(captures, ref_date)
            record.update(summary)
        records.append(record)

    #+==========================
    #: today activity summary
    activity_summary, activity_stats = [], _()
    captures = list(db.Capture.get_by_date(ref_date.isoformat(), paginate=False))
    if captures:
        activity_stats = stats.day_activity_stats(captures, ref_date)
        activity_breakdown = stats.day_activity_breakdown(captures, ref_date)
        for record in activity_breakdown:
            activity_summary.append(_(record))

    return {
        'is_front': True, 
        'title': 'Capture Summary',
        'records': records,
        'activity_records': activity_summary,
        'activity_stats': activity_stats,
        'report_ref_date': ref_date,
        'report_weekdate_bounds': wkdate_bounds,
    }


@route('/xforms/')
@view('xforms')
def xforms():
    forms = db.XForm.get_all(include_inactive=True)
    return {
        'title': 'XForms',
        'records': forms
    }      


@post('/xforms/')
def xforms_sync():
    if 'sync' in request.forms:
        forms = api.get_xforms()
        failed, reports = [], []

        for f in forms:
            exist = db.XForm.get_by_id(f['id_string'])
            if exist: 
                continue
        
            try:
                f['date_created'] = datetime.now().strftime(FMT_SHORTDATE)
                f['active'] = False
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


@route('/xforms/<form_id>/')
@view('xform-capture-summary')
def xform_info(form_id):
    xform = db.XForm.get_by_id(form_id)
    captures = db.Capture.get_by_form(form_id, paginate=False)
    summaries = stats.summary_by_day(captures)

    return {
        'title': 'Daily Summary',
        'sync_records': [],
        'records': summaries,
        'xform': xform
    }

@post('/xforms/<form_id>/')
def xform_capture_sync(form_id):
    from services import api2
    from services import transform

    sync_date = request.forms.get('sync_date')
    id_string = request.forms.get('id_string')

    dt = datetime.today().date().isoformat()
    activity = {
        'date_created': dt,
        'sync_date': sync_date,
        'sync_table': 'f130_cf05_KN',            
        'record_count': 0,
    }

    transformed = []
    for captures in api2.get_captures(activity):
        if captures:
            for capture in captures:
                transformed.append(transform.to_flatten_dict(capture))
            
            db.Capture.save_many(transformed)
        transformed=[]
    return 'Done'
