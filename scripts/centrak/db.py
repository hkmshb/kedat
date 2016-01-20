"""
Data access provider.
"""
import pymongo
from datetime import datetime

import settings
from utils import paginate
from kedat.core import Storage as _


# connection
conn = pymongo.MongoClient()
db = conn.test_centrak



class XForm:

    @staticmethod
    def get_all(include_inactive=False):
        qry = {} if include_inactive else {'active': True}
        cur = db.xforms.find(qry)\
                .sort('id', pymongo.ASCENDING)
        return paginate(cur)
    
    @staticmethod
    def get_by_id(id):
        record = db.xforms.find_one({'id_string': id })
        return _(record or {})

    @staticmethod
    def insert_one(record):
        return db.xforms.insert_one(record)
    
    @staticmethod
    def set_active(id, status):
        return db.xforms.update_one(
            {'id_string': id},
            {'$set': {'active': status}}
        )


class Capture:

    @staticmethod
    def get_by_form(form_id, paginate=True):
        cur = db.captures.find({'_xform_id_string': form_id})
        return paginate(cur) if paginate else cur

    @staticmethod
    def get_by_date(ref_date, paginate=True):
        cur = db.captures.find({'datetime_today': ref_date})
        return paginate(cur) if paginate else cur

    @staticmethod
    def save_many(records):
        db.captures.insert_many(records)
