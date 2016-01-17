"""
Routes and views for the bottle application.
"""
from datetime import datetime
from bottle import post, route, request, response, redirect
from bottle import view as view_fn

import db
import settings
from services.forms import SyncForm
from services import api, stats, tasks, transform


DATE_FMT='%Y-%m-%d'

def view(tpl_name):
    context = {
        'request': request,
        'year': datetime.now().year,
    }
    return view_fn(tpl_name, **context)


@route('/')
@view('index')
def index():
    form_id = 'f000_cf04_KN'
    result = tasks.get_form_summary(form_id)
    return {
        'title': 'Capture Summary',
        'records': result
    }


@route('/home2')
@view('index2')
def home():
    """Renders the home page."""
    # display summary for most recent captures
    form_id = 'f000_cf04_KN'
    summary_type = db.SUMMARY_MONTH

    results = stats.summarize_capture(form_id, db.SUMMARY_WEEK)
    return {
        'title': 'Capture Summary',
        'records': results[0] or [],
        'ind_summary': results[1],
        'team_summary': results[2],
        'summary_type': ('Today'
            if summary_type == db.SUMMARY_TODAY
            else 'This Week' if summary_type == db.SUMMARY_WEEK
            else 'This Month')
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

            if captures:
                for capture in captures:
                    transformed.append(transform.to_flatten_dict(capture))
                
                # save transformed documents    
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
    }


@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
    )


@route('/home-orig')
@view('index-orig')
def home_orig():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )