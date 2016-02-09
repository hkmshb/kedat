from bottle import HTTPError
from kedat.core import Storage as _
import db


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
        instance, fields = _(), ['_id','code','name','capacity','vratio','source_feeder']
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

