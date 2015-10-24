"""
Ad-hoc kedat script for working with power network data.
"""
import os
from enum import Enum

from pymongo import MongoClient
from kedat.core import XlSheet, Storage as _



def load_mongodb_with_transmission_network_assets():
    # setup mongodb stuff
    client = MongoClient('mongodb://localhost:27017')
    db = client.kedco    
    
    # helper method
    def save_station(station):
        db.stations.insert_one(station)
        print('station inserted: %s' % station.name)
        print('  --- transforms: %s, feeders: %s' % (
                len(station.transformers),
                sum([len(t.feeders) for t in station.transformers])))
    
    base_dir = os.path.dirname(os.path.dirname(__file__)) 
    data_dir = os.path.join(base_dir, '..', 'kedco_data')
    filepath = os.path.join(data_dir, 'kedco-ntwk-assets.xlsx')
    
    ws = XlSheet(filepath, 'TStations+Fdrs')
    
    # find and extract all headers using sample headers
    sample_hdrs = ['sn','ts.name','xfmr.id']
    hdr_idx = XlSheet.find_headers(ws, sample_hdrs, 0)
    if hdr_idx == -1:
        raise Exception("Headers not found: %s" % sample_hdrs)
    
    # iterate rows, extract data & push into db.stations collection
    class cols: # enum class for col-index 
        (ts_name, xfmr_id, xfmr_cap) = range(1, 4)
        (fdr_volt, fdr_name, fdr_code) = range(6, 9)
    
    station, feeders = None, None
    for row in ws:
        if row[cols.ts_name] != None:
            # new station read; save collected station details (if any)
            if station:
                save_station(station)
            
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
        save_station(station)




if __name__ == '__main__':
    load_mongodb_with_transmission_network_assets()
    print('done!')
