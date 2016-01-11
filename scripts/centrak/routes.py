"""
Routes and views for the bottle application.
"""

from bottle import route, view
from datetime import datetime
import services
import db



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