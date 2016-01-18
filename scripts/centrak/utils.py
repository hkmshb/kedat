﻿"""
Defines utility functions and classes.
"""
import os
from datetime import datetime
from dateutil import relativedelta as rd
from bottle import request

from kedat.core import Storage as _
import settings



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


def paginate(cursor, qs_page='pg', qs_page_size='pg_size'):
    size = request.get(qs_page_size, settings.PAGE_SIZE)
    page = request.get(qs_page, 1)

    paginator = Paginator(cursor, size)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)
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
            return (self.number * self.p.page_size)

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

