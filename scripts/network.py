"""
Ad-hoc kedat script for working with power network data.
"""
import os
import pymongo
from openpyxl import load_workbook

from kedat.core import XlSheet, Storage as _



#: directory paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'kedco_data')


#: constants
TRANSMISSION = 0
INJECTION    = 1
DISTRIBUTION = 2

SOURCE_TYPES = (
    TRANSMISSION,
    INJECTION,
    DISTRIBUTION
)


class Reader:
    
    def __init__(self, ws, source_type):
        if source_type not in SOURCE_TYPES:
            raise ValueError('Invalid source type provided')
        self.source_type = source_type
        self.ws = ws
    
    def get_assets(self):
        assets_gen = lambda x:[]
        if self.source_type == TRANSMISSION:
            assets_gen = self._get_transmission_assets
        elif self.source_type == INJECTION:
            assets_gen = self._get_injection_assets
        elif self.source_type == DISTRIBUTION:
            assets_gen = self._get_distribution_assets 
        
        cols = self._get_cols_index_info()
        return assets_gen(cols)
    
    def _ensure_headers_exist(self, sample_headers, row_offset=0):
        """Returns the index at which provided headers are found, otherwise
        an exception is raised.
        """
        index = XlSheet.find_headers(self.ws, sample_headers, row_offset)
        if index == -1:
            raise Exception("Headers not found: %s" % sample_headers)
        return index
    
    def _get_row_entry(self, row, label, default=''):
        return row[label] or default
    
    def _get_cols_index_info(self):
        names, indexes = (), ()
        if self.source_type == TRANSMISSION:
            names = ('ts_code', 'ts_name', 'ts_loc', 'xfmr_id', 'xfmr_cap', 
                     'fdr_volt', 'fdr_name', 'fdr_code')
            indexes = list(range(1, 6)) + list(range(9, 12))
        elif self.source_type == INJECTION:
            names = ('source', 'is_code', 'is_name', 'is_loc', 'is_type', 
                     'xfmr_id', 'xfmr_cap', 'fdr_code', 'fdr_volt', 'fdr_name')
            indexes = list(range(1, 8)) + list(range(11, 14))
        elif self.source_type == DISTRIBUTION:
            names = ('fdr_volt', 'fdr_name', 'ss_name', 'ss_cap', 'ss_type')
            indexes = list(range(1, 3)) + list(range(4, 7))
        return _(zip(names, indexes))
    
    def _get_transmission_assets(self, cols):
        # helper
        get = self._get_row_entry
        
        # find headers
        hdrs = ['sn', 'ts.code', 'ts.name', 'ts.loc', 'xfmr.id']
        self._ensure_headers_exist(hdrs)
        
        # iterate rows and extract asset in nested-form
        station, feeders = None, None
        for row in self.ws:
            # new station encountered?
            if get(row, cols.ts_name):
                if station:
                    yield station
                
                station = _({
                    'code': get(row, cols.ts_code),
                    'name': get(row, cols.ts_name),
                    'location': get(row, cols.ts_loc),
                    'type': 'transmission',
                    'transformers': []
                })
            
            # new transformer encountered?
            if get(row, cols.xfmr_id):
                feeders = []
                station.transformers.append(_({
                    'name': get(row, cols.xfmr_id),
                    'capacity': get(row, cols.xfmr_cap),
                    'feeders': feeders
                }))
            
            # collect feeder details
            feeders.append(_({
                'code': get(row, cols.fdr_code),
                'voltage': get(row, cols.fdr_volt),
                'name': get(row, cols.fdr_name).strip().title()
            }))
        
        # return very last station
        if station:
            yield station
    
    def _get_injection_assets(self, cols):
        # helper
        get = self._get_row_entry
        
        # find headers
        hdrs = ['sn', 'source', 'is.code', 'is.name', 'is.loc', 'is.type']
        self._ensure_headers_exist(hdrs)
        
        # iterate rows, extract data & push into collection
        station, feeders, count = None, None, 0
        for row in self.ws:
            # new station encountered
            if row[cols.source] != None:
                if station: 
                    yield station
                
                is_public = get(row, cols.is_type).lower() == 'p'
                count += 1
                station = _({
                    'code': get(row, cols.is_code),
                    'name': get(row, cols.is_name),
                    'location': get(row, cols.is_loc),
                    'type': 'injection',
                    'source_feeder': get(row, cols.source),
                    'is_public': is_public,
                    'transformers': []
                })
            
            # new transformer encountered
            if row[cols.xfmr_id] != None:
                feeders = []
                station.transformers.append(_({
                    'name': get(row, cols.xfmr_id),
                    'capacity': get(row, cols.xfmr_cap),
                    'feeders': feeders
                }))
            
            if is_public:
                feeders.append(_({
                    'code': get(row, cols.fdr_code),
                    'voltage': get(row, cols.fdr_volt),
                    'name': get(row, cols.fdr_name).strip().title()
                }))
        
        # return very last station
        if station:
            yield station
    
    def _get_distribution_assets(self, cols):
        # helper
        get = self._get_row_entry
        
        # find headers
        hdrs = ['fdr.sn', 'fdr.volt', 'fdr.name', 'ss.sn']
        self._ensure_headers_exist(hdrs)
        
        # iterate rows and extract asset in nested-form
        source_feeder, skip_count = None, 0
        for row in self.ws:
            # new source_feeder encountered
            if get(row, cols.fdr_name):
                source_feeder = _({
                    'volt': get(row, cols.fdr_volt),
                    'name': get(row, cols.fdr_name).strip().title(),
                })
            
            # ensure a source_feeder exist at this point otherwise
            # ignore current line and proceed to the next line even 
            # if it has substation details.
            if not source_feeder:
                skip_count += 1
                continue
            
            ## from original list sub-station name needs to be normalized
            ss_name = get(row, cols.ss_name).title().strip()
            if ss_name.endswith(','):
                ss_name = (ss_name[:-1]).strip()
            
            is_public = get(row, cols.ss_type).lower() == 'p'
            station = _({
                'code': 'Sx',
                'name': ss_name,
                'type': 'distribution',
                'source_feeder': source_feeder.name,
                'is_public': is_public,
                'transformers': [_({
                    'name': 'TR1',
                    'capacity': get(row, cols.ss_cap),
                    'upriser_count': 0
                })]
            })
            yield station
        print('# lines skipped: %s' % skip_count)


class Loader:
    
    @staticmethod
    def _save_asset(db, asset):
        db.assets.insert_one(asset)
        msg_fmt = 'assets:: station: {0:<30}, transformers: {1:<3}, feeders: {2:<3}'
        args = (asset.name, len(asset.transformers),
                sum([len(t.feeders) for t in asset.transformers]))
        print(msg_fmt.format(*args))

    @staticmethod
    def load_network_assets(db, wb):
        args_list = (
            (TRANSMISSION, 'TStations+Fdrs'),
            (INJECTION,    'IStations+Fdrs')
        )
        for args in args_list:
            ws = XlSheet(wb, args[1])
            reader = Reader(ws, args[0])
            for asset in reader.get_assets():
                Loader._save_asset(db, asset)
    
    @staticmethod
    def _save_as_stations_feeders(db, asset):
        def split(asset):
            feeders = []
            for t in asset.transformers:
                for feeder in t.feeders:
                    f = feeder.copy()
                    f.update({
                        'source': {
                            'station': asset.code,
                            'transformer': t.name
                        }
                    })
                    feeders.append(f)
                del t['feeders']
            return (asset, feeders)
        
        station, feeders = split(asset)
        db.stations.insert(station)
        
        if feeders:
            db.feeders.insert_many(feeders)
        
        msg_fmt = 'assets:: station: {0:<30}, transformers: {1:<3}, feeders: {2:<3}'
        args = (station.name, len(station.transformers), len(feeders))
        print(msg_fmt.format(*args))
    
    @staticmethod
    def _loadMV_network_stations_feeders(db, wb):
        args_list = (
            (TRANSMISSION, 'TStations+Fdrs'),
            (INJECTION,    'IStations+Fdrs')
        )
        for args in args_list:
            ws = XlSheet(wb, args[1])
            reader = Reader(ws, args[0])
            for asset in reader.get_assets():
                Loader._save_as_stations_feeders(db, asset)
    
    @staticmethod
    def _loadLV_network_stations(db, wb):
        # extra 11kV feeder list from db
        cursor = db.feeders\
                   .find({'voltage':11, 'name': {'$ne': ''}})\
                   .sort('name', pymongo.ASCENDING)
        
        feeders = {f['name']:f['code'] for f in cursor}
        
        # get dist. sub-stations from file
        assets, not_found, xlfeeders = [], [], set()
        ws = XlSheet(wb, 'DStations-11KV')
        reader = Reader(ws, DISTRIBUTION)
        for asset in reader.get_assets():
            assets.append(asset)
            
            # change feeder name to feeder code
            name = asset['source_feeder']
            xlfeeders.add(name)
            if name not in feeders:
                not_found.append(name)
            else:
                asset['source_feeder'] = feeders[name]
            
            # save to db
            db.stations.insert_one(asset)
        print('assets:: stations: %s' % len(assets))


def run(task):
    filename = os.path.join(DATA_DIR, 'kedco-ntwk-assets.xlsx')
    wb = load_workbook(filename)
    db = pymongo.MongoClient().kedco
    
    task(db, wb)


def clear_mongo_db(db, wb):
    db.stations.delete_many({})
    db.feeders.delete_many({})


def collect_injss_sorted(db, wb):
    cursor = db.stations\
               .find({'type':'injection'})\
               .sort([('is_public', pymongo.ASCENDING),
                      ('location', pymongo.ASCENDING),
                      ('name', pymongo.ASCENDING)])

    with open(os.path.join(DATA_DIR, 'injss-sorted.txt'), 'w') as f:
        for station in cursor:
            f.write('{}, {}, {}\n'.format(
                'p' if station['is_public'] else 'd',
                station['location'],
                station['name']
            ))
        f.flush()


