﻿import os, sys
from bottle import HTTPError
from collections import OrderedDict
from kedat.core import Storage as _
import db

from services import choices


class FormBase:
    def __init__(self, request):
        self.request = request
        self._instance = None
        self.errors = []

    def is_valid(self):
        pass


class ProjectForm(FormBase):
    
    def is_valid(self):
        _id = self.request.forms.get('_id', '').strip()
        id  = self.request.forms.get('id', '').strip()
        name = self.request.forms.get('name', '').strip()
        xforms = self.request.forms.getall('xforms')
        uforms = self.request.forms.getall('uforms')

        if not id:
            self.errors.append('Project Id required')
        if not name:
            self.errors.append('Project name required.')
        if self.errors:
            return False

        self._instance = _(
            _id=_id, id=id, name=name, 
            xforms=xforms, uforms=uforms
        )
        return True

    def save(self):
        if not self._instance:
            raise HTTPError(500, "Invalid operation performed.")

        _id = self._instance._id
        del self._instance['_id']

        if not _id:
            db.Project.insert_one(self._instance)
        else:
            db.Project.update_one(self._instance)


class FeederForm(FormBase):
    def is_valid(self):
        instance, fields = _(), ['_id','code','name','voltage','source']
        for f in fields:
            instance[f] = self.request.forms.get(f, '').strip()
        
        if not instance.code:
            self.errors.append('Feeder code required')
        if not instance.name:
            self.errors.append('Feeder name required')
        if not instance.voltage:
            self.errors.append('Feeder voltage required')

        self._instance = instance
        return (len(self.errors) == 0)

    def save(self):
        if not self._instance:
            raise HTTPError(500, "Invalid operation performed.")

        if not self._instance._id:
            db.Feeder.insert_one(self._instance)
        else:
            db.Feeder.update_one(self._instance)


class StationForm(FormBase):
    def is_valid(self):
        instance, fields = _(), ['_id','code','name','capacity','vratio','public','source_feeder']
        for f in fields:
            instance[f] = self.request.forms.get(f, '').strip()

        if not instance.code:
            self.errors.append('Station code required.')
        if not instance.name:
            self.errors.append('Station name required.')
        if not instance.capacity:
            self.errors.append('Station capacity required.')
        if not instance.vratio:
            self.errors.append('Station voltage ratio required.')
        if not instance.source_feeder:
            self.errors.append('Station source feeder required.')

        self._instance = instance
        return (len(self.errors) == 0)

    def save(self):
        if not self._instance:
            raise HTTPError(500, "Invalid operation performed.")

        if not self._instance._id:
            db.Station.insert_one(self._instance)
        else:
            db.Station.update_one(self._instance)


class StationImportForm(FormBase):

    def __init__(self, request, file_ext, max_file_size=None):
        super(StationImportForm, self).__init__(request)
        if not file_ext:
            raise ValueError("`file_ext` required to indicate expected file extension.")
        
        if not file_ext.startswith('.'):
            file_ext = '.%s' % file_ext

        self.max_file_size = max_file_size
        self.file_ext = file_ext.lower()

    def is_valid(self):
        instance, fields = _(), ['impfile']
        for f in fields:
            instance[f] = self.request.files.get(f, _())

        if not instance.impfile:
            self.errors.append("File upload required.")
        
        filename = instance.impfile.filename.lower()
        name, ext = os.path.splitext(filename)
        if self.file_ext != ext:
            msg_fmt = "File with extension '%s' expected but '%s' provided"
            self.errors.append(msg_fmt % (self.file_ext, ext))

        if self.max_file_size:
            uploaded_size = sys.getsizeof(instance.impfile.file)
            if uploaded_size > self.max_file_size:
                msg_fmt = "Maximum file size exceeded. Expected: %s, Actual: %s"
                self.errors.append(msg_fmt % (self.max_file_size, uploaded_size))

        self._instance = instance
        return (len(self.errors) == 0)

        
class CaptureForm(FormBase):
    _meta = _({
        'fields': OrderedDict([
            ('capture', OrderedDict([
                ('_project_id','Project Id'), 
                ('_enum_id','Enumerator Id'), 
                ('_group','Group Name'), 
                ('rseq','Route Seq'), 
                ('_station','Station Code'),
                ('_upriser','Upriser Code'), 
                ('_datetime_start','Date Time Start'), 
                ('_datetime_end','Date Time End'), 
                ('_datetime_today','Capture Date')])),
            ('plot', OrderedDict([
                ('plot_type','Plot Type'), 
                ('occupant','Occupant Status'), 
                ('new_tholder','New Title Holder')])),
            ('address', OrderedDict([
                ('addy_no','House #'), 
                ('addy_street','Street'), 
                ('addy_town_city','Town/City'),
                ('addy_state','State'), 
                ('addy_lga','LGA'), 
                ('addy_landmark','Closest Landmark'), 
                ('gps','GPS')])),
            ('customer', OrderedDict([
                ('cust_name','Customer Name'), 
                ('cust_mobile1','Mobile #1'), 
                ('cust_mobile2','Mobile #2'),
                ('cust_email','Email')])),
            ('account', OrderedDict([
                ('acct_no', 'Account #'), 
                ('acct_status', 'Account Status'),
                ('book_code','Book Code'),
                ('tariff', 'Tariff'),
                ('tariff_new', 'New Tariff'),
                ('amt_4_adc', 'Amount for ADC')])),
            ('meter', OrderedDict([
                ('meter_no', 'Meter #'),
                ('meter_phase','Meter Phase'), 
                ('meter_type','Meter Type'),
                ('meter_status','Meter Status'),
                ('meter_model', 'Meter Model'),
                ('meter_accessible', 'Is Accessible'),
                ('meter_brand', 'Meter Brand'),
                ('meter_cert_no', 'Meter Cert. #'),
                ('meter_extra1', 'Meter Extra 1'),
                ('meter_extra2', 'Meter Extra 2'),
                ('meter_location1','Location #1'),
                ('meter_location2','Location #2'),
                ('meter_manuf_date', 'Manufacture Date'),
                ('meter_seal_location', 'Seal Location'),
                ('meter_seal_no', 'Seal #'),
                ('meter_seal_property', 'Seal Property')])),
            ('supply', OrderedDict([
                ('supply_source', 'Supply Source'),
                ('alt_power_source', 'Alternate Source'),
                ('multi', 'Multiple Source'),
                ('neighbour_rseq', 'Neighbour R.Seq')])),
            ('billing', OrderedDict([
                ('current_bill', 'Current Bill'),
                ('outstanding_amt','Outstanding Amount'),
                ('last_payment','Last Payment'), 
                ('proposed_bill','Proposed Bill Amount'), 
                ('bill_assessment', 'Bill Assessment')])),
            ('meta', OrderedDict([
                ('_attachments','Attachements'), 
                ('_duration','Duration'), 
                ('_notes','Notes'), 
                ('_status','Status'),
                ('_submission_time','Submission Time'), 
                ('_submitted_by','Submitted By'), 
                ('_tags','Tags'), 
                ('_uuid','UUID'),
                ('_version','Version'), 
                ('_xform_id_string','XForm Id'), 
                ('device_imei','Device IMEI')])),
        ]),
        'widgets': OrderedDict({
            'select': ['acct_status', 'tariff', 'tariff_new', 'meter_type', 
                'meter_phase', 'meter_brand', 'meter_status', 'meter_location1', 
                'plot_type', 'supply_source', 'bill_assessment', 'cust_assessment',
                'occupant', 'addy_state', 'addy_lga'],
            'multi-select': ['alt_power_source', 'remarks'],
        }),
    })

    def render_field(self, name, record):
        tags = 'id="id_{0}" name="{0}" class="form-control{1}"'
        if name in self._meta.fields['meta']:
            return '<label {0}>{1}</label>'.format(
                tags.format(name, '-static'),
                record.get(name, '-'))
        elif name in self._meta.widgets['select'] or \
             name in self._meta.widgets['multi-select']:
            multi =( name in self._meta.widgets['multi-select'])
            tags = [tags.format(name, ''), 'multi=""' if multi else '']
            options = self.build_select_options(name, record)
            xml = '<select {0}>{1}</select>'.format(
                        ' '.join(tags),
                        options)
            return xml

        tags = [tags.format(name, '')]
        tags.append('type="{0}"'.format(
            'date' if 'date' in name else 'text'))
        
        if name.startswith('_'):
            tags.append('readonly=""')

        field_name = name[1:] if name.startswith('_') else name
        tags.append('value="{0}"'.format(record.get(field_name, '-')))
        return '<input {0} />'.format(' '.join(tags))

    def build_select_options(self, name, record):
        tags, options = [], []
        if hasattr(choices, name.upper()):
            options = getattr(choices, name.upper())

        tag = '<option value="{0}" {2}>{1}</option>'
        tags.append(tag.format('', '&laquo; Select One &raquo;', ''))
        for value, text in options:
            args = [value, text, '']
            if value == record.get(name, '-'):
                args[2] = 'selected=""'
            tags.append(tag.format(*args))
        return ''.join(tags)

