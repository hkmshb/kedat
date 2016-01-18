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
    def get_all():
        cur = db.xforms.find({})\
                .sort('id', pymongo.ASCENDING)
        return paginate(cur)
    
    @staticmethod
    def get_by_id(id):
        return _(db.xforms.find_one({'id': id }))

    @staticmethod
    def insert_one(record):
        return db.xforms.insert_one(record)
    
    @staticmethod
    def set_active(id, status):
        try:
            id = int(id)
            return db.xforms.update_one(
                {'id': id},
                {'$set': {'active': status}}
            )
        except:
            return 0
                
        

