﻿"""
Routes and views for the bottle application.
"""
from datetime import datetime, date
from bottle import HTTPError, post, route, request, response, redirect
from requests.exceptions import ConnectionError
from kedat.core import Storage as _

import db                
from utils import get_session, write_log, get_weekdate_bounds, view,\
     _get_ref_date
from services import api, stats, transform, report
from settings import FMT_SHORTDATE
from routes import authnz, authorize



@route('/')
@view('index')
def index():
    #+==========================
    #: forms series summary
    records = []
    projects = db.Project.get_all()
    ref_date = _get_ref_date()
    wkdate_bounds = get_weekdate_bounds(ref_date)

    for p in projects:
        record = _(id=p.id, name=p.name)
        captures = db.Capture.get_by_project(p.id, paginate=False)
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


@route('/projects/')
@view('projects')
def projects():
    records = []
    projects = db.Project.get_all()

    for p in projects:
        record = _(id=p.id, name=p.name)
        captures = db.Capture.get_by_project(p.id, paginate=False)
        if captures.count():
            summary = stats.activity_summary(captures)
            record.update(summary)
        records.append(record)

    return {
        'title': 'Projects',
        'records': records
    }


@route('/projects/<project_id>/')
@view('project-view')
@authorize()
def project_view(project_id):
    project = db.Project.get_by_id(project_id)
    xrecords, urecords = [], []

    for f in project.xforms:
        xform = db.XForm.get_by_id(f)
        record = _(id=xform.id_string, title=xform.title)
        captures = db.Capture.get_by_form(f, False)
        if captures.count():
            summary = stats.activity_summary(captures)
            record.update(summary)
        xrecords.append(record)

    for f in project.uforms:
        uform = db.XForm.get_by_id(f)
        record = _(id=uform.id_string, title=uform.title)
        updates = db.Update.get_by_form(f, False)
        if updates.count():
            summary = stats.activity_summary(updates)
            record.update(summary)
        urecords.append(record)

    return {
        'title': 'Project: %s' % project.name,
        'project': project,
        'xrecords': xrecords,
        'urecords': urecords
    }


@post('/projects/<project_id>/sync')
@authorize(role='moderator')
def project_sync(project_id):
    p = db.Project.get_by_id(project_id)
    if not p:
        raise HTTPError(404, 'Project not found: %s' % project_id)

    messages = get_session()['messages']
    form_type, xforms_to_sync = None, None
    for key in ['project_xforms', 'project_uforms']:
        if key in request.forms:
            form_type = key
            xforms_to_sync = request.forms.get(key).split(',')

    sync_target = (db.Capture if form_type == 'project_xforms' else db.Update)

    # get form count
    for xform_id in xforms_to_sync:
        count = sync_target.count_by_form(xform_id)
        xform = db.XForm.get_by_id(xform_id)

        # pull new captures
        try:
            transformed, pull_count = [], 0
            for captures in api.get_captures(xform.id, start=count):
                if captures:
                    pull_count += len(captures)
                    for c in captures:
                        transformed.append(transform.to_flatten_dict(c))

                    sync_target.save_many(transformed)
                    transformed = []

            messages['pass'].append('%s captures pulled.' % pull_count)
        except ConnectionError:
            messages['fail'].append('Sync failed. Internet connection required.')
        except Exception as ex:
            messages['fail'].append('Sync failed. %s' % str(ex))

    return redirect('/projects/%s/' % project_id)


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


@post('/r/default/')
@authorize(role='moderator')
def report_default():
    messages = get_session()['messages']

    project_id = request.forms.get('project_id')
    ref_date = request.forms.get('ref_date')

    try:
        report.write_report(project_id, ref_date)
        messages['pass'].append('Report generated.')
    except Exception as ex:
        messages['fail'].append('Report generation failed. %s' % str(ex))
        print(ex)
    return redirect('/')

