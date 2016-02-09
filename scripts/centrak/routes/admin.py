"""
Routes and views for admin access.
"""
from bottle import HTTPError, post, route, request, redirect
from requests import ConnectionError
import pymongo

from kedat.core import Storage as _
from routes import authnz, authorize
from utils import view, get_session
from services import api
import db, forms



@route('/admin/')
@view('admin/index')
@authorize(role='moderator')
def index():
    return {
        'title': 'Admin',
        'stat': _({
            'count_xforms': db.XForm.count(),
            'count_projects': db.Project.count()
        })
    }


@route('/admin/projects/')
@view('admin/projects')
@authorize(role='moderator')
def projects():
    def func(xforms):
        def f(id):
            for xf in xforms:
                if xf.id_string == id:
                    return xf.title
            return ''
        return f

    projects = db.Project.get_all(include_inactive=True)
    xforms = db.XForm.get_all(include_inactive=True)
    return {
        'title': 'Projects', 'records': projects,
        'get_xform_title': func(xforms),
    }


@route('/admin/projects/create', method=['GET', 'POST'])
@route('/admin/projects/<id>/', method=['GET', 'POST'])
@view('admin/project-form')
@authorize(role='moderator')
def manage_project(id=None):
    project = _(xforms=[], uforms=[]) if not id else db.Project.get_by_id(id)
    if not project:
        raise HTTPError(404, "Project not found: %s" % id)

    xforms = db.XForm.get_unassigned_xforms(False, False)
    uforms = db.XForm.get_unassigned_uforms(False, False)
    session = get_session()
        
    if request.method == 'POST':
        form = forms.ProjectForm(request)
        try:
            if form.is_valid():
                form.save()
                action = ('created' if not id else 'updated')
                session['messages']['pass'].append('Project %s' % action)
            else:
                session['messages']['fail'].extend(form.errors)

            return redirect('/admin/projects/')
        except pymongo.errors.DuplicateKeyError:
            session['messages']['fail'].append("Provided Project Id and/or Name already exists.")
            project = form._instance

    return {
        'title':'Projects',
        'project': project,
        'xforms': [_(f) for f in xforms],
        'uforms': [_(f) for f in uforms],
    }


@route('/admin/xforms/')
@view('admin/xforms')
@authorize(role='moderator')
def xforms():
    forms = db.XForm.get_all(include_inactive=True)
    return { 'title':'XForms', 'records': forms }


@post('/admin/xforms/sync')
@authorize(role='moderator')
def xforms_sync():
    failed, reports = [], []
    session = get_session()
    messages = session['messages']

    try:
        for forms in api.get_xforms():
            for f in forms:
                exist = db.XForm.get_by_id(f['id_string'])
                if exist: 
                    continue
        
                try:
                    f['active'] = False
                    db.XForm.insert_one(f)
                except Exception as ex:
                    failed.append(f)
                    reports.append(str(ex))

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
    except ConnectionError as ex:
        messages['fail'].append('Connection Error. Unable to establish '
                                'Internet connection.')
    return redirect('/admin/xforms/')


@post('/admin/xforms/update')
@authorize(role='moderator')
def xforms_update():
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
    return redirect('/admin/xforms/')


@route('/admin/feeders/')
@view('admin/feeders')
@authorize(role='moderator')
def feeders():
    feeders = db.Feeder.get_all(include_inactive=True)
    return {
        'title': 'Feeders', 'records': feeders,
    }


@route('/admin/feeders/<code>/')
@view('admin/feeder-view')
@authorize(role='moderator')
def feeder_view(code):
    def get_vratio_display(vratio):
        for i, text in db.Volt.CHOICES:
            if vratio == str(i):
                return text
        return None

    feeder = db.Feeder.get_by_code(code)
    stations = db.Station.get_by_feeder(code)
    return {
        'title': 'Feeder',
        'feeder': feeder,
        'stations': stations,
        'get_vratio_display': get_vratio_display
    }


@route('/admin/feeders/create', method=['GET', 'POST'])
@route('/admin/feeders/<code>/edit', method=['GET', 'POST'])
@view('admin/feeder-form')
@authorize(role='moderator')
def manage_feeder(code=None):
    feeder = _() if not code else db.Feeder.get_by_code(code)
    if code and not feeder:
        raise HTTPError(404, "Feeder not found: %s" % id)

    session = get_session()        
    if request.method == 'POST':
        form = forms.FeederForm(request)
        try:
            if form.is_valid():
                form.save()
                action = ('created' if not code else 'updated')
                session['messages']['pass'].append('Feeder %s' % action)
            else:
                session['messages']['fail'].extend(form.errors)

            return redirect('/admin/feeders/')
        except pymongo.errors.DuplicateKeyError:
            session['messages']['fail'].append("Provided Feeder Code and/or Name already exists.")
            feeder = form._instance

    return {
        'title':'Projects',
        'feeder': feeder,
    }


@route('/admin/feeders/<feeder_code>/station/create', method=['GET','POST'])
@route('/admin/feeders/<feeder_code>/station/<code>/', method=['GET','POST'])
@view('admin/station-form')
@authorize(role='moderator')
def manage_station(feeder_code, code=None):
    feeder = db.Feeder.get_by_code(feeder_code)
    if not feeder:
        raise HTTPError(404, "Feeder not found: %s" % feeder_code)

    station = _() if not code else db.Station.get_by_code(code)
    if code and not station:
        raise HTTPError(404, "Station not found: %s" % code)

    session = get_session()['messages']
    if request.method == 'POST':
        form = forms.StationForm(request)
        try:
            if form.is_valid():
                form.save()
                action = ('created' if not code else 'updated')
                session['pass'].append('Station %s' % action)
            else:
                session['fail'].extend(form.errors)
            return redirect('/admin/feeders/%s/' % feeder_code)
        except pymongo.errors.DuplicateKeyError:
            session['fail'].append("Provided Station Code already exists.")
            station = form._instance
    
    return {
        'title': 'Station',
        'station': station,
        'feeder': feeder,
        'vratio_choices': db.Volt.CHOICES,
    }
