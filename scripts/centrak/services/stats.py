import pandas as pd
from datetime import datetime

import db
import utils
from kedat.core import Storage as _



def series_purity_summary(records, ref_date=None):
    df = pd.DataFrame(list(records))
    result, key = _(), 'datetime_today'
    if not ref_date:
        ref_date = datetime.now().date()

    if 'last_updated' not in df.columns:
        df['last_updated'] = None

    if 'is_junk' not in df.columns:
        df['is_junk'] = None

    # today
    f = df[df[key] == ref_date.isoformat()]
    result.update(_purity_summary(f, 'd'))

    # week
    dates = utils.get_weekdate_bounds(ref_date)
    f = df[df[key] >= dates[0].isoformat()]
    f = f[f[key] <= dates[1].isoformat()]
    print(f)
    result.update(_purity_summary(f, 'w'))

    # month
    dates = utils.get_monthdate_bounds(ref_date)
    f = df[df[key] >= dates[0].isoformat()]
    f = f[f[key] <= dates[1].isoformat()]
    result.update(_purity_summary(f, 'm'))

    # all
    result.update(_purity_summary(df, ''))
    return result


def _purity_summary(df, prefix):
    result, key = _(), 'datetime_today'
    result['%s_total' % prefix] = df[key].size

    # duplicate rseq check
    key = 'rseq'
    f = df[df.duplicated(key) == True]
    result['%s_rseq_duplicates' % prefix] = f[key].size

    # duplicate acct_no check
    key = 'acct_no'
    f = df[df[key].isnull() == False]
    f = f[f.duplicated(key) == True]
    result['%s_acctno_duplicates' % prefix] = f[key].size

    # fixed/updated records
    key = 'last_updated'
    f = df[df[key].isnull() == False]
    result['%s_updated' % prefix] = f[key].size

    # junk records
    key = 'is_junk'
    f = df[df[key].isnull() == False]
    result['%s_junk' % prefix] = f[key].size
    return result

