import pandas as pd
from datetime import datetime
from dateutil import relativedelta as rd
from db import Capture
import db
from kedat.core import Storage as _



DATE_FMT = '%Y-%m-%d'


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


def summarize_simple(frame):
    result = _()
    result.update(summarize_duplicates(frame))
    result.update(summarize_acct_status(frame))
    result.update(summarize_meter_type(frame))
    result.update(summarize_meter_status(frame))
    result.update(summarize_valid_gps(frame))
    return result


def summaize_totals(frame):
    result, now = _(), datetime.now()
    result.all = frame['datetime_today'].size

    start_date = now.strftime(DATE_FMT)
    f = frame[frame['datetime_today'] == start_date]
    result.today = f['datetime_today'].size

    start_date = (now + rd.relativedelta(weekday=rd.MO)).strftime(DATE_FMT)
    end_date = (now + rd.relativedelta(weekday=rd.FR)).strftime(DATE_FMT)
    f = frame[frame['datetime_today'] >= start_date]
    f = f[f['datetime_today'] <= end_date]
    result.week = f['datetime_today'].size

    start_date = (now + rd.relativedelta(day=1)).strftime(DATE_FMT)
    end_date = (now + rd.relativedelta(day=31)).strftime(DATE_FMT)
    f = frame[frame['datetime_today'] >= start_date]
    f = f[f['datetime_today'] <= end_date]
    result.month = f['datetime_today'].size
    return result


def summarize_duplicates(frame):
    result = _()
    
    # duplicate rseq
    f = frame[frame.duplicated('rseq') == True]
    result.rseq_duplicates = f['rseq'].size

    # duplicate acct_no
    f = frame[frame['acct_no'].isnull() == False]
    f = f[f.duplicated('acct_no') == True]
    result.acct_no_duplicates = f['acct_no'].size
    return result


def summarize_acct_status(frame):
    result = _()
    keys = ['unknown', 'new', 'active', 'inactive', 'not-conn', 
            'disconn-bill', 'disconn-no-bill', 'n_a']

    for key in keys:
        f = frame[frame['acct_status'] == key]
        result[key.replace('-','_')] = f['acct_status'].size

    # active count decomposed
    f = frame[frame['acct_status'] == 'active']
    ff = f[f['meter_type'] == 'ppm']
    result.active_ppm = ff['acct_status'].size
    result.active_analogue = result.active - result.active_ppm

    return result


def summarize_meter_type(frame):
    result = _()
    for key in ['none', 'analogue', 'ppm']:
        f = frame[frame['meter_type'] == key]
        result[key] = f['meter_type'].size
    return result


def summarize_meter_status(frame):
    result = _()
    keys = ['unknown', 'none', 'n-a', 'ok' 'bypass']
    for key in keys:
        f = frame[frame['meter_status'] == key]
        result[key.replace('-','_')] = f['meter_status'].size
    return result


def summarize_meter_phase(frame):
    result = _()
    for key in ['1-phase', '3-phase']:
        f = frame[frame['meter_phase'] == key]
        new_key = 'meter_%s' % key.replace('-','_')
        result[new_key] = f['meter_phase'].size
    return result


def summarize_valid_gps(frame):
    f = frame[frame['gps'][3] > 5.0]
    return _(gps_invalid = f['gps'].size)
