import db
import pandas as pd
from . import stats



def get_form_summary(form_id):
    # get all captures for form
    captures = db.Capture().get_all(form_id)

    # summary form
    f = pd.DataFrame(captures)
    results = stats.summaize_totals(f)
    results.form = form_id
    return [results]
