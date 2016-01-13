import pandas as pd
from datetime import datetime
from dateutil import relativedelta as rd
from db import Capture
import db
from kedat.core import Storage as _


def summarize_capture(form_id, summary_type):
    records = Capture().get_all(form_id)
    df = pd.DataFrame(records)

    # perform grouping then summarize
    groups = df.groupby('datetime_today')
    icount = groups['rseq'].count()

    df['enum_id2'] = df['enum_id'].apply(lambda x: x.strip().upper())
    df['team'] = df['enum_id'].apply(lambda x: x.split('/')[0])

    groups2 = df.groupby('enum_id2')
    icount2 = groups2['enum_id2'].size()

    group3 = df.groupby('team')
    icount3 = group3['team'].size()

    summaries = []
    for i in range(len(icount)):
        summary = _(date=icount.index[i], total=icount[i])        
        gdf = groups.get_group(icount.index[i])

        # get no. duplicates
        flt = gdf[gdf.duplicated('rseq') == True]
        summary.duplicated = flt['rseq'].size

        flt = gdf[gdf['acct_no'].isnull() == False]
        flt = flt[flt.duplicated('acct_no') == True]
        summary.dup_accts = flt['acct_no'].size

        # get no. new customers
        flt = gdf[gdf['acct_status'] == 'new']
        summary.new = flt['acct_status'].size

        flt = gdf[gdf['acct_status'] == 'active']
        flt = flt[flt['meter_type'] != 'ppm']
        summary.active = flt['acct_status'].size

        flt = gdf[gdf['meter_type'] == 'ppm']
        summary.ppms = flt['meter_type'].size

        flt = gdf[gdf['acct_no'].isnull() == False]
        summary.accts = flt['acct_no'].size
        summaries.append(summary)
        
    return (summaries, icount2, icount3)






    

