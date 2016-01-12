"""
Routes and views for the bottle application.
"""
from datetime import datetime
from bottle import post, route, request, response, redirect
from bottle import view as view_fn

import db
import settings
from services.forms import SyncForm
from services import api
from services import transform


DATE_FMT='%Y-%m-%d'

def view(tpl_name):
    return view_fn(tpl_name, request=request)


@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    # display summary for most recent captures
    form_id = 'f000_cf04_KN'
    dao = db.CaptureSummary()
    
    summary_type = db.SUMMARY_TODAY
    captures = dao.get_today(form_id)
    if not captures:
        summary_type = db.SUMMARY_WEEK
        captures = dao.get_this_week(form_id)

    return {
        'title': 'Capture Summary',
        'year': datetime.now().year,
        'records': captures or [],
        'summary_type': ('Today'
            if summary_type == db.SUMMARY_TODAY
            else 'This Week')
    }


@route('/activities')
@view('activities')
def activities():
    # paging control
    page = request.query.page or '1'
    page_size = settings.PAGE_SIZE

    dao = db.Activity()    
    records = dao.get_all(page, page_size)
    return {
        'title': 'Activities',
        'year': datetime.now().year,
        'activities': records
    }


@post('/activities')
def perform_activity():
    dao = db.Activity()
    form = SyncForm(request)
    
    if form.is_valid():
        activity = dao.get(form.sync_table, form.sync_date)
        found = True
        if not activity:
            found = False
            activity = {
                'date_created': datetime.now().strftime(DATE_FMT),
                'sync_date': form.sync_date.strftime(DATE_FMT),
                'sync_table': form.sync_table,            
                'record_count': 0,
            }
        
        dao_capture = db.Capture()
        transformed, count, chunk = ([], 0, 1)
        print('sync in progress...')
        for captures in api.get_captures(activity):
            print('chunk {0:0>2}: processing...'.format(chunk), end='')
            count += len(captures)

            for capture in captures:
                transformed.append(transform.to_flatten_dict(capture))
            
            dao_capture.save_many(transformed)
            print(', saved (%s)' % len(captures))
            transformed = []
            chunk += 1

        # update activity record
        activity['record_count'] = count
        dao.save(activity)
        
        form.messages['__all__'].append('Sync was successful.')
        form.messages.save()
        return redirect('/activities')

    return {
        'title': 'Activities',
        'year': datetime.now().year,
    }


@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )


@route('/home-orig')
@view('index-orig')
def home_orig():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )