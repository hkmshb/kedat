"""
Provides validation and other services for forms.
"""
from datetime import datetime
from bottle import request


class BaseForm:

    def __init__(self, request):
        self.request = request
        self.messages = request.environ.get('beaker.session')
        self.messages['__all__'] = []        
        self.messages['errors'] = []

    def _get_fields(self):
        raise NotImplementedError()


class SyncForm(BaseForm):
    
    def __init__(self, request):
        super(SyncForm, self).__init__(request)
        self.sync_table = None
        self.sync_date = None

    def is_valid(self):
        sync_date = request.forms.get('sync_date')
        sync_table = request.forms.get('sync_table')

        if not sync_date and not sync_table:
            self.messages['errors'].extend([
                'Sync date needs to be provided.',
                'Select a sync table',
            ])
            self.messages.save()
            return False;

        try:
            sync_date = datetime.strptime(sync_date, '%Y-%m-%d')
        except:
            self.messages['errors'].append('Invalid date format.')
            self.messages.save()
            return false
        
        self.sync_table = sync_table
        self.sync_date = sync_date
        return True


        


