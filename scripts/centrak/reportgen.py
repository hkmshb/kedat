"""
Ad-hoc csv report generation script.
"""
import os, sys
import argparse
from datetime import datetime

import pandas as pd
import db


BASE_DIR = os.path.dirname(__file__)
REPORT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..', '..', '_reports'))

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
   

def run(args, target_dir, date_digits):
    captures = db.Capture.get_by_date(args.ref_date, False)
    df = pd.DataFrame(list(captures))

    filename = os.path.join(target_dir, ('error-rpt-%s.xls' % date_digits))
    writer = pd.ExcelWriter(filename)

    print('Generating Reports for: %s' % args.ref_date)
    if args.dup_rseq or args.all:
        print('compiling duplicate rseq records...')
        try:
            result = get_duplicate_rseqs(df)
            sheet_name = 'duplicate-rseq'
            result.to_excel(writer, sheet_name=sheet_name)
            print('sucess: records written\r\n')
        except Exception as ex:
            print('fail: %s\r\n' % str(ex))

    if args.dup_acct or args.all:
        print('compiling duplicate acct records...')
        try:
            result = get_duplicate_accts(df)
            sheet_name = 'duplicate-acct'
            result.to_excel(writer, sheet_name=sheet_name)
            print('success: records written\r\n')
        except Exception as ex:
            print('failed: %s\r\n' % str(ex))
    
    if args.invalid_station or args.all:
        print('compiling invalid station records...')
        try:                                                                    
            result = get_invalid_stations(df, args.invalid_station)
            sheet_name = 'invalid-stations'
            result.to_excel(writer, sheet_name=sheet_name)
            print('success: records written\r\n')
        except Exception as ex:
            print('failed: %s\r\n' % str(ex))
    
    # flush all writes to disk
    writer.save()



if __name__ == '__main__':
    # define parser
    parser = argparse.ArgumentParser(description="Report Generation Script")
    add = parser.add_argument
    add('-d', '--ref-date', nargs='?', default=datetime.now().date().isoformat(),
        help="Date for which to produce report")
    add('--dup-rseq', action='store_true',
        help="Product duplicate route-sequence report")
    add('--dup-acct', action='store_true', help="Produce duplicate accounts report")
    add('--invalid-station', nargs='*', help="Product invalid station report")
    add('-a', '--all', action='store_true', help="Product all forms of report")

    args = parser.parse_args()
    date_digits = args.ref_date.replace('-','')

    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
            
    run(args, REPORT_DIR, date_digits)
