"""
Ad-hoc csv report generation script.
"""
import os, sys
import pandas as pd
from datetime import datetime

import db

BASE_DIR = os.path.dirname(__file__)
REPORT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..', '..', '_reports'))

ref_date = datetime.now().date().isoformat()
rpt_cols = ['rseq', 'enum_id', 'cust_name', 'addy_house_no', 'addy_street',
            'acct_status', 'acct_no', 'current']

def get_duplicate_rseqs(df):
    key = 'rseq'
    d = df[df.duplicated(key) == True]
    duplicates = pd.DataFrame()
    for v in d[key].values:
        duplicates = duplicates.append(df[df[key] == v][rpt_cols])

    for col in rpt_cols:
        duplicates[col] = duplicates[col].apply(lambda x: str(x).upper())
    return duplicates


def get_duplicate_accts(df):
    key = 'acct_no'
    f = df[df[key].isnull() == False]
    d = f[f.duplicated(key) == True]
    
    duplicates = pd.DataFrame()
    for v in d[key].values:
        duplicates = duplicates.append(df[df[key] == v][rpt_cols])
    
    for col in rpt_cols:
        duplicates[col] = duplicates[col].apply(lambda x: str(x).upper())
    return duplicates


def get_invalid_stations(df, codes):
    if not codes:
        raise ValueError('Invalid codes not provided')
    
    key = 'station'
    df[key] = df['rseq'].apply(lambda x: x.upper().split('/')[0])
    records = pd.DataFrame()
    for v in [c.upper() for c in codes]:
        records = records.append(df[df[key] == v][[key] + rpt_cols])

    for col in ([key] + rpt_cols):
        records[col] = records[col].apply(lambda x: str(x).upper())
    return records
    

def run(argv, target_dir, date_digits):
    captures = db.Capture.get_by_date(ref_date, False)
    df = pd.DataFrame(list(captures))

    if '--duplicate-rseq' in argv or '--all' in argv:
        print('compiling duplicate rseq records...')
        try:
            result = get_duplicate_rseqs(df)
            filename = 'duplicate-rseq-%s.csv' % date_digits
            result.to_csv(os.path.join(target_dir, filename))
            print('sucess: records written\r\n')
        except Exception as ex:
            print('fail: %s\r\n' % str(ex))

    if '--duplicate-accts' in argv or '--all' in argv:
        print('compiling duplicate acct records...')
        try:
            result = get_duplicate_accts(df)
            filename = 'duplicate-acct-%s.csv' % date_digits
            result.to_csv(os.path.join(target_dir, filename))
            print('success: records written\r\n')
        except Exception as ex:
            print('failed: %s\r\n' % str(ex))
    
    if '--invalid-stations' in argv or '--all' in argv:
        print('compiling invalid station records...')
        try:
            result = get_invalid_stations(df, argv[1:])
            filename = 'invalid-stations-%s.csv' % date_digits
            result.to_csv(os.path.join(target_dir, filename))
            print('success: records written\r\n')
        except Exception as ex:
            print('failed: %s\r\n' % str(ex))



if __name__ == '__main__':
    date_digits = ref_date.replace('-','')
    TARGET_DIR = os.path.join(REPORT_DIR, date_digits)

    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
            
    run(sys.argv[1:], TARGET_DIR, date_digits)
