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
db = conn.centrak



class Project:
    
    @staticmethod
    def count():
        return db.projects.count({})

    @staticmethod
    def get_all(include_inactive=True, paginate=True):
        qry = {} if include_inactive else {'active': True}
        cur = db.projects.find(qry)\
                .sort('id', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_by_id(id):
        record = db.projects.find_one({'id': id})
        return _(record or {})

    @staticmethod
    def insert_one(record):
        tdy = datetime.today().date().isoformat()
        record['date_created'] = tdy
        record['last_modified'] = None
        return db.projects\
                 .insert_one(record)
    
    @staticmethod
    def set_active(id, status):
        tdy = datetime.today().date().isoformat()
        return db.projects\
                 .update_one(
            {'id': id},
            {'$set': {
                'active': status,
                'last_modified': tdy}
            }
        )
    
    @staticmethod
    def update_one(record):
        tdy = datetime.today().date().isoformat()
        record['last_modified'] = tdy
        return db.projects\
                 .update({'id': record.id}, record)


class XForm:

    @staticmethod
    def count(include_inactive=False):
        qry = {} if include_inactive else {'active': True}
        return db.xforms.count(qry)

    @staticmethod
    def get_all(include_inactive=False, paginate=True):
        qry = {} if include_inactive else {'active': True}
        cur = db.xforms.find(qry)\
                .sort('id', pymongo.DESCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_unassigned_xforms(include_inactive=False, paginate=True):
        xforms = []
        for p in Project.get_all(paginate=False):
            xforms.extend(p['xforms'])

        qry = {'id': {'$nin': xforms}}
        if not include_inactive:
            qry.update({'active': True})

        cur = db.xforms.find(qry)\
                .sort('id', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_unassigned_uforms(include_inactive=False, paginate=True):
        uforms = []
        for p in Project.get_all(paginate=False):
            uforms.extend(p['uforms'])

        qry = {'id': {'$nin': uforms}, 'id_string': {'$regex': 'f[0-9]{3}_cu.+'}}
        if not include_inactive:
            qry.update({'active': True})

        cur = db.xforms.find(qry)\
                .sort('id', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur
  
    @staticmethod
    def get_by_id(id):
        record = db.xforms.find_one({'id_string': id })
        return _(record or {})

    @staticmethod
    def insert_one(record):
        tdy = datetime.today().date().isoformat()
        record['date_created'] = tdy
        record['last_modified'] = None
        return db.xforms\
                 .insert_one(record)
    
    @staticmethod
    def set_active(id, status):
        tdy = datetime.today().date().isoformat()
        return db.xforms.update_one(
            {'id_string': id},
            {'$set': {
                'active': status,
                'last_modified': tdy }
            }
        )


class CaptureBase:
    
    def __init__(self, collection_name):
        self._collection_name = collection_name
    
    @property
    def db(self):
        return db[self._collection_name]
        
    def count_by_date(self, ref_date):
        return self.db\
                   .count({'datetime_today': ref_date})

    def count_by_date_form(self, ref_date, ref_id):
        return self.db\
                   .count({'datetime_today': ref_date,
                           '_xform_id_string': ref_id })
    
    def count_by_form(self, ref_id):
        return self.db\
                   .count({'_xform_id_string': ref_id})

    def get_by_date(self, ref_date, paginate=True):
        cur = self.db\
                  .find({'datetime_today': ref_date})\
                  .sort('rseq', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    def get_by_date_form(self, ref_date, ref_id, paginate=True):
        cur = self.db\
                  .find({'datetime_today': ref_date,
                         '_xform_id_string': ref_id})
        return utils.paginate(cur) if paginate else cur

    def get_by_form(self, ref_id, paginate=True):
        cur = self.db\
                  .find({'_xform_id_string': ref_id})\
                  .sort((['datetime_today', pymongo.ASCENDING],
                         ['rseq', pymongo.ASCENDING]))
        return utils.paginate(cur) if paginate else cur

    def get_by_project(self, pjt_id, paginate=True):
        cur = self.db\
                  .find({'project_id': pjt_id})\
                  .sort('date_created', pymongo.DESCENDING)
        return utils.paginate(cur) if paginate else cur

    def save_many(self, records):
        self.db\
            .insert_many(records)


class UpdateBase(CaptureBase):

    def __init__(self):
        super(UpdateBase, self).__init__('updates')

    def insert_one(self, record):
        transform = self._transform(record)
        self.db\
            .insert_one(transform)

    def save_many(self, records):
        for record in records:
            self.insert_one(record)

    def _transform(self, record):
        return record


Capture = CaptureBase('captures')
Update = UpdateBase()
