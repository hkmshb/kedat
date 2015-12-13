"""
Ad-hoc kedat script for working with power network data.
"""
import os
from pymongo import MongoClient
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
        
        cols = self._get_cols_index_info()
        return assets_gen(cols)
    
    def _get_cols_index_info(self):
        names, indexes = (), ()
        if self.source_type == TRANSMISSION:
            names = ('ts_code', 'ts_name', 'xfmr_id', 'xfmr_cap', 
                     'fdr_volt', 'fdr_name', 'fdr_code')
            indexes = list(range(1, 5)) + list(range(8, 11))
        elif self.source_type == INJECTION:
            names = ('source', 'is_name', 'is_type', 'xfmr_id', 'xfmr_cap',
                     'fdr_code', 'fdr_volt', 'fdr_name')
            indexes = list(range(1, 6)) + list(range(9, 12))
        return _(zip(names, indexes))
    
    def _get_transmission_assets(self, cols):
        # helper
        get = lambda r, label: r[label] or ''
        
        # find headers
        hdrs = ['sn', 'ts.code', 'ts.name', 'xfmr.id']
        if not XlSheet.find_headers(self.ws, hdrs, 0):
            raise Exception("Headers not found: %s" % hdrs)
        
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
                'name': get(row, cols.fdr_name)
            }))
        
        # return very last station
        if station:
            yield station
    
    def _get_injection_assets(self, cols):
        # helper
        get = lambda r, label: r[label] or ''
        
        # find headers
        hdrs = ['sn', 'source', 'is.name', 'is.type']
        if not XlSheet.find_headers(self.ws, hdrs, 0):
            raise Exception("Headers not found: %s" % hdrs)
        
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
                    'code': 'IS{:0>2}'.format(hex(count)[2:]).upper(),
                    'name': get(row, cols.is_name),
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
                    'name': get(row, cols.fdr_name)
                }))
        
        # return very last station
        if station:
            yield station


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
            db.feeders.insert(feeders)
        
        msg_fmt = 'assets:: station: {0:<30}, transformers: {1:<3}, feeders: {2:<3}'
        args = (station.name, len(station.transformers), len(feeders))
        print(msg_fmt.format(*args))
    
    @staticmethod
    def _load_network_stations_feeders(db, wb):
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
    def load():
        filename = os.path.join(DATA_DIR, 'kedco-ntwk-assets.xlsx')
        wb = load_workbook(filename)
        db = MongoClient().kedco
        
        Loader._load_network_stations_feeders(db, wb)


if __name__ == '__main__':
    Loader.load()
    pass

