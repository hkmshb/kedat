"""
Ad-hoc kedat script for working with power network data.
"""
import os
from pymongo import MongoClient
from openpyxl import load_workbook

from kedat.core import XlSheet, Storage as _
from builtins import staticmethod


class Network:
    
    @staticmethod
    def _save_station(db, station):
        db.stations.insert_one(station)
        print('station inserted: %s' % station.name)
        print('  --- transformers: %s' % len(station.transformers))
        print('  -------- feeders: %s' % (
                sum([len(t.feeders) for t in station.transformers])))
    
    @staticmethod
    def _load_transmission_assets(db, wb):
        ws = XlSheet(wb, 'TStations+Fdrs')
        
        # find and extract all headers using sample headers
        sample_hdrs = ['sn','ts.name','xfmr.id']
        hdr_idx = XlSheet.find_headers(ws, sample_hdrs, 0)
        if hdr_idx == -1:
            raise Exception("Headers not found: %s" % sample_hdrs)
        
        # iterate rows, extract data & push into db.stations collection
        class cols:     # enum class for col-index 
            (ts_name, xfmr_id, xfmr_cap) = range(1, 4)
            (fdr_volt, fdr_name, fdr_code) = range(7, 10)
        
        station, feeders = None, None
        for row in ws:
            if row[cols.ts_name] != None:
                # new station read; save collected station details (if any)
                if station:
                    Network._save_station(db, station)
                
                station = _({
                    'name': row[cols.ts_name],
                    'type': 'transmission', 
                    'transformers': []
                })
            
            if row[cols.xfmr_id] != None:
                # new equipment read; add collected equipment detail
                feeders = []
                station.transformers.append(_({
                    'name': row[cols.xfmr_id],
                    'capacity': row[cols.xfmr_cap],
                    'feeders': feeders 
                }))
            
            feeders.append({
                'code': row[cols.fdr_code],
                'voltage': row[cols.fdr_volt],
                'name': row[cols.fdr_name]
            })
        
        # save last station collected
        if station:
            Network._save_station(db, station)
    
    @staticmethod
    def _load_injection_assets(db, wb):
        ws = XlSheet(wb, 'IStations+Fdrs')
        
        # find and extract all headers using sample headers
        sample_hdrs = ['sn', 'source', 'is.name', 'is.type']
        hdr_idx = XlSheet.find_headers(ws, sample_hdrs, 0)
        if hdr_idx == -1:
            raise Exception("Headers not found: %s" % sample_hdrs)
        
        # iterate rows, extract data & push into db.stations collection
        class cols:     # enum class for col-index]
            (source, is_name, is_type, xfmr_id, xfmr_cap) = range(1, 6)
            (fdr_code, fdr_volt, fdr_name) = range(8, 11)
        
        station, feeders = None, None
        for row in ws:
            if row[cols.source] != None:
                # new station read; save collected station details (if any)
                if station:
                    Network._save_station(db, station)
                
                is_public = row[cols.is_type].lower() == 'p'
                station = _({
                    'name': row[cols.is_name],
                    'type': 'injection',
                    'source_feeder': row[cols.source],
                    'is_public': is_public,
                    'transformers': []
                })
            
            if row[cols.xfmr_id] != None:
                # new transformer read; add collected transformer detail
                feeders = []
                station.transformers.append(_({
                    'name': row[cols.xfmr_id],
                    'capacity': row[cols.xfmr_cap],
                    'feeders': feeders
                }))
            
            if is_public:
                feeders.append({
                    'code': row[cols.fdr_code],
                    'voltage': row[cols.fdr_volt],
                    'name': row[cols.fdr_name]
                })
        
        # save last station collected
        if station:
            Network._save_station(db, station)
    
    @staticmethod
    def load_assets():
        # setup mongodb stuff
        client = MongoClient('mongodb://localhost:27017')
        db = client.kedco
        
        # load workbook
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(base_dir, '..', 'kedco_data')
        filepath = os.path.join(data_dir, 'kedco-ntwk-assets.xlsx')
        
        wb = load_workbook(filepath)
        Network._load_transmission_assets(db, wb)
        Network._load_injection_assets(db, wb)


class NetworkExt:
    
    @staticmethod
    def _save_station(db, station):
        db.stations.insert_one(station)
        print(': station inserted: %s' % station.name)
        print('+ --- transformers: %s' % len(station.transformers))
    
    @staticmethod
    def _save_feeders(db, feeders):
        db.feeders.insert(feeders)
        print('+ -------- feeders: %s' % len(feeders))
    
    @staticmethod
    def _load_transmission_assets(db, wb):
        ws = XlSheet(wb, 'TStations+Fdrs')
        
        # find and extract all headers using sample headers
        sample_hdrs = ['sn', 'ts.name', 'xfmr.id']
        if not XlSheet.find_headers(ws, sample_hdrs, 0):
            raise Exception('Headers not found: %s' % sample_hdrs)
        
        # iterate rows, extract data & push into collections
        class cols:     # enum class for col-index
            (ts_name, xfmr_id, xfmr_cap) = range(1, 4)
            (fdr_volt, fdr_name, fdr_code) = range(7, 10)
        
        station, transformer, feeders = None, None, None
        for row in ws:
            if row[cols.ts_name] != None:
                # new station encountered;
                if station:
                    NetworkExt._save_station(db, station)
                    if feeders:
                        NetworkExt._save_feeders(db, feeders)
                
                feeders = []
                station = _({
                    'name': row[cols.ts_name],
                    'type': 'transmission',
                    'transformers': []
                })
            
            if row[cols.xfmr_id] != None:
                # new equipment encountered
                transformer = _({
                    'name': row[cols.xfmr_id],
                    'capacity': row[cols.xfmr_cap],
                })
                station.transformers.append(transformer)
            
            feeders.append({
                'code': row[cols.fdr_code] or '',
                'voltage': row[cols.fdr_volt],
                'name': row[cols.fdr_name] or '',
                'source': {
                    'station': station.name,
                    'transformer': transformer.name
                }
            })
        
        # save last station and feeders encountered
        if station:
            NetworkExt._save_station(db, station)
        
            if feeders:
                NetworkExt._save_feeders(db, feeders)
    
    @staticmethod
    def _load_injection_assets(db, wb):
        ws = XlSheet(wb, 'IStations+Fdrs')
        
        # find and extract all headers using sample headers
        sample_hdrs = ['sn', 'source', 'is.name', 'is.type']
        if not XlSheet.find_headers(ws, sample_hdrs, 0):
            raise Exception('Headers not found: %s' % sample_hdrs)
        
        # iterate rows, extract data & push into collections
        class cols:     # enum class for col-index
            (source, is_name, is_type, xfmr_id, xfmr_cap) = range(1, 6)
            (fdr_code, fdr_volt, fdr_name) = range(9, 12)
        
        station, transformer, feeders = None, None, None
        for row in ws:
            if row[cols.source] != None:
                # new station encountered
                if station:
                    NetworkExt._save_station(db, station)
                    if feeders:
                        NetworkExt._save_feeders(db, feeders)
                
                is_public = row[cols.is_type].lower() == 'p'
                feeders= []
                station = _({
                    'name': row[cols.is_name],
                    'type': 'injection',
                    'source_feeder': row[cols.source],
                    'is_public': is_public,
                    'transformers': []
                })
            
            if row[cols.xfmr_id] != None:
                # new transformer encountered
                transformer = _({
                    'name': row[cols.xfmr_id],
                    'capacity': row[cols.xfmr_cap]
                })
                station.transformers.append(transformer)
            
            if station.is_public:
                feeders.append({
                    'code': row[cols.fdr_code] or '',
                    'voltage': row[cols.fdr_volt],
                    'name': row[cols.fdr_name] or '',
                    'source': {
                        'station': station.name,
                        'transformer': transformer.name,
                    }
                })
        
        # save last station and feeders encountered
        if station:
            NetworkExt._save_station(db, station)
            if feeders:
                NetworkExt._save_feeders(db, feeders)
    
    @staticmethod
    def load_assets():
        conn = MongoClient('mongodb://localhost:27017')
        db = conn.kedco_ext
        
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(base_dir, '..', 'kedco_data')
        filepath = os.path.join(data_dir, 'kedco-ntwk-assets.xlsx')
        
        wb = load_workbook(filepath)
        NetworkExt._load_transmission_assets(db, wb)
        NetworkExt._load_injection_assets(db, wb)


if __name__ == '__main__':
    NetworkExt.load_assets()
    print('done!')
