﻿"""
Defines utility functions and classes.
"""
import os
import pymongo
from datetime import datetime
from dateutil import relativedelta as rd
from bottle import request, view as fn_view

from kedat.core import Storage as _
import settings



def view(tmpl_name):
    ref_date = _get_ref_date()
    wkdate_bounds = get_weekdate_bounds(ref_date)

    context = {
        'year': datetime.now().year,
        'get_session': get_session,
        'get_authnz': get_authnz,
        'request': request,
        
        # calendar entries
        'ref_date': ref_date,
        'weekdate_bounds': wkdate_bounds,
    }
    return fn_view(tmpl_name, **context)


def write_log(lines):
    try:
        filepath = os.path.join(settings.BASE_DIR, 'centrak.error.log')
        stamp = datetime.now().isoformat()
        with open(filepath, 'a') as f:
            f.write('\r\n'.join([('[%s]: %s' % (stamp, line)) for line in lines]))
            f.flush()
    except Exception as ex:
        print("*"*80)
        print("WRITING TO LOG FAILED.\r\n\t%s" % str(ex))
        print("LOG LINES:\r\n%s" % ('\t'.join(lines)))
        print()


def _get_ref_date():
    try:
        ref_date = request.query.get('refdate', None)
        ref_date = (datetime.strptime(ref_date, '%Y%m%d').date()
                    if ref_date else datetime.today().date())
    except:
        ref_date = datetime.today().date()
    return ref_date


def get_session():
    """Retrieves the session object"""
    session = request.environ.get('beaker.session')
    if 'messages' not in session:
        session['messages'] = _({
            'pass': [], 
            'fail': [], 
            'warn': []
        })
        session.save()
    return session


def get_authnz():
    from routes import authnz
    return authnz


def make_auth_decorator(cork, username=None, role=None, fixed_role=False, 
                        fail_unauth_redirect='/login', 
                        fail_auth_redirect='/restricted'):
    """
    Extends the default function by same name provided by bottle-cork where
    non authenticated users are asked to login and authenticated users with
    less access permission get an 'Access Restricted' messages.
    """
    def auth_required(username=username, role=role, fixed_role=fixed_role,
                      fail_redirect=fail_unauth_redirect):
        def decorator(func):
            import functools

            @functools.wraps(func)
            def wrapper(*a, **kw):
                redirect_url = fail_redirect
                if not cork.user_is_anonymous:
                    redirect_url = fail_auth_redirect

                cork.require(
                    username=username, role=role, fixed_role=fixed_role,
                    fail_redirect=redirect_url)
                return func(*a, **kw)
            return wrapper
        return decorator
    return auth_required


def get_weekdate_bounds(ref_date):
    start_date = ref_date
    if ref_date.weekday() > 0:
        start_date = ref_date + rd.relativedelta(weekday=rd.MO(-1))
    end_date = ref_date + rd.relativedelta(weekday=rd.SU)
    return (start_date, end_date)


def get_monthdate_bounds(ref_date):
    start_date = ref_date + rd.relativedelta(day=1, month=ref_date.month)
    end_date = ref_date + rd.relativedelta(day=31, month=ref_date.month)
    return (start_date, end_date)


def paginate(cursor, size=None, qs_page='page', qs_page_size='pageSize'):
    size = request.query.get(qs_page_size, size or settings.PAGE_SIZE)
    page = request.query.get(qs_page, 1)

    paginator = Paginator(cursor, size)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)
    
    # extend page further
    p.current_page_size = size
    num_pages = p.paginator.num_pages
    p.paging_numbers = [
        1,
        1 if not p.has_previous() else p.previous_page_number(),
        num_pages if not p.has_next() else p.next_page_number(),
        num_pages
    ]   
    return p


class EmptyPage(Exception):
    pass


class PageNotAnInteger(Exception):
    pass


class Paginator:

    class Page:
        
        def __init__(self, paginator, number):
            self.p = paginator
            self.number = number
            self.cache = None
        
        def __iter__(self):
            for item in self.object_list:
                yield item

        def __bool__(self):
            return len(self.object_list) > 0
        
        @property
        def paginator(self):
            return self.p

        @property
        def object_list(self):
            if not self.cache:
                try:
                    p = self.p
                    skip_size = self.start_index() - 1
                    cursor = p.cursor\
                              .skip(skip_size)\
                              .limit(p.page_size)
                    items = [_(item) for item in cursor]
                except Exception as ex:
                    items = []
                self.cache = items
            return self.cache

        def has_next(self):
            return (self.number < len(self.p.page_range))

        def has_previous(self):
            return (self.number > 1)

        def has_other_pages(self):
            return (len(self.p.page_range) > 1)

        def next_page_number(self):
            next = self.number + 1
            if next <= len(self.p.page_range):
                return next
            raise EmptyPage()

        def previous_page_number(self):
            prev = self.number - 1
            if prev > 0:
                return prev
            raise EmptyPage()
        
        def start_index(self):
            return ((self.number - 1) * self.p.page_size) + 1

        def end_index(self):
            return min((self.number * self.p.page_size), self.p.count)

    def __init__(self, cursor, page_size):
        self.cursor = cursor
        self.page_size = page_size

        # figures
        self.count = cursor.count()
        self.num_pages = self._get_chunk_count(self.count, page_size)
        self.page_range = range(self.num_pages)

    def page(self, number):
        try:
            number = int(number)
            return Paginator.Page(self, number)
        except:
            raise PageNotAnInteger()

    def _get_chunk_count(self, total, size):
        q, r = int(total / size), (total % size)
        return (q if r == 0 else (q + 1))


class MongoDbSetupMiddleware:

    def __init__(self, app):
        self.wrapped_app = app

    def __call__(self, environ, start_response):
        self._create_indexes()
        return self.wrapped_app(environ, start_response)
    
    def _create_indexes(self):
        from db import db
        IndexModel = pymongo.IndexModel
        ASC = pymongo.ASCENDING

        # projects collection
        indexes = [IndexModel([('id', ASC)], unique=True),
                   IndexModel([('name', ASC)], unique=True)]
        db.projects.create_indexes(indexes)

        # xforms collection
        indexes = [IndexModel([('id_string', ASC)]),
                   IndexModel([('id', ASC)], unique=True),
                   IndexModel([('title', ASC)], unique=True)]
        db.xforms.create_indexes(indexes)

        # captures
        indexes = [IndexModel([('rseq', ASC)]),
                   IndexModel([('group', ASC)]),
                   IndexModel([('acct_no', ASC)]),
                   IndexModel([('substation', ASC)]),
                   IndexModel([('meter_type', ASC)]),
                   IndexModel([('meter_phase', ASC)]),
                   IndexModel([('acct_status', ASC)]),
                   IndexModel([('cust_mobile1', ASC)])]
        db.captures.create_indexes(indexes)

