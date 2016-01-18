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
