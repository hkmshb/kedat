"""
Data access provider.
"""
import pymongo
from datetime import datetime

import utils
import settings
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
        return utils.paginate(cur)
    
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
    def count_by_date(ref_date):
        return db.captures\
                 .count({'datetime_today': ref_date})

    @staticmethod
    def count_by_date_form(ref_date, ref_id):
        return db.captures\
                 .count({'datetime_today': ref_date,
                         '_xform_id_string': ref_id })
    
    @staticmethod
    def count_by_form(ref_id):
        return db.captures\
                 .count({'_xform_id_string': ref_id})

    @staticmethod
    def get_by_date(ref_date, paginate=True):
        cur = db.captures\
                .find({'datetime_today': ref_date})\
                .sort('rseq', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_by_date_form(ref_date, ref_id, paginate=True):
        cur = db.captures\
                .find({'datetime_today': ref_date,
                       '_xform_id_string': ref_id})
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_by_form(ref_id, paginate=True):
        cur = db.captures\
                .find({'_xform_id_string': ref_id})\
                .sort((['datetime_today', pymongo.ASCENDING],
                       ['rseq', pymongo.ASCENDING]))
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def save_many(records):
        db.captures.insert_many(records)
