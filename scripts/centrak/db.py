"""
Data provider.
"""
import pymongo
from datetime import datetime
from kedat.core import Storage as _
from dateutil import relativedelta as rd


# consts
SUMMARY_TODAY = 1
SUMMARY_WEEK  = 2
SUMMARY_MONTH = 3

SUMMARY_LIST = (
    (SUMMARY_TODAY, 'Today'),
    (SUMMARY_WEEK, 'This Week'),
    (SUMMARY_MONTH, 'This Month')
)


DATE_FMT = '%Y-%m-%d'


# connection
conn = pymongo.MongoClient()
db = conn.test_centrak


class CaptureSummary:

    def get_today(self, form_id):
        return self.get_by_date(form_id, datetime.now())

    def get_this_week(self, form_id):
        wk_start = datetime.now()
        wk_end = (datetime.now() + rd.relativedelta(rd.FR))
        return self.get_by_date_range(form_id, wk_start, wk_end)

    def get_by_date(self, form_id, value=None):
        if not value:
            raise ValueError('value must be provided')

        cursor = db.summary.find({
            'form_id': form_id,
            'datetime_today': value.strftime(DATE_FMT)
        })
        return self._get_records(cursor)

    def get_by_date_range(self, form_id, from_value, to_value):
        cursor = db.summary.find({
            'form_id': form_id,
            'datetime_today': {'$gte': from_value.strftime(DATE_FMT) },
            'datetime_today': {'$lte': to_value.strftime(DATE_FMT) },
        })
        return self._get_records(cursor)

    def _get_records(self, cursor):
        records = []
        for entry in cursor:
            records.append(_({
                'total': entry['total'],
                'duplicates': entry['duplicates'],
                'billable': entry['billable'],
                'revisits': entry['revisits'],
            }))
        return records
