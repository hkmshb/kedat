"""
Routes and views for the bottle application.
"""
from datetime import datetime, date
from bottle import post, route, request, response, redirect, template
from requests.exceptions import ConnectionError
from kedat.core import Storage as _

import db                
from utils import get_session, write_log, get_weekdate_bounds, view,\
     _get_ref_date
from services import api, stats, transform, report
from settings import FMT_SHORTDATE



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
        failed, reports = [], []

        for forms in api.get_xforms():
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


@post('/xforms/<id_string>/')
def xform_capture_sync(id_string):
    xform = db.XForm.get_by_id(id_string)
    session = get_session()

    if not xform:
        session['messages']['warn'].append('XForm with specified id not found')
    else:
        date_captured = request.forms.get('date_captured')
        #id_string = request.forms.get('id_string')

        # get item count
        count = db.Capture.count_by_date_form(date_captured, id_string)
        print('.. %s, %s, %s' % (date_captured, id_string, count))

        # pull new captures
        try:
            transformed, pull_count = [], 0
            for captures in api.get_captures(xform['id'], date_captured, start=count):
                if captures:
                    pull_count += len(captures)
                    for c in captures:
                        transformed.append(transform.to_flatten_dict(c))

                    db.Capture.save_many(transformed)
                    transformed = []

            session['messages']['pass'].append('%s captures pulled.' % pull_count)
        except ConnectionError:
            session['messages']['fail'].append('Sync failed: connection error.')
        except Exception as ex:
            session['messages']['fail'].append('Sync failed: %s' % str(ex))
    

    return redirect('/xforms/%s/' % id_string)


@post('/r/default/')
def report_default():
    ref_date = request.forms.get('ref_date')
    form_id = request.forms.get('form_id')

    report.write_report(form_id, ref_date)
    session = get_session()
    session['messages']['pass'].append('Report generated.')
    return redirect('/')


