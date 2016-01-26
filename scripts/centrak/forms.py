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

        if not id:
            self.errors.append('Project Id required')
        if not name:
            self.errors.append('Project name required.')
        if self.errors:
            return False

        self._instance = _(_id=_id, id=id, name=name, xforms=xforms)
        return True

    def save(self):
        if not self._instance:
            raise HTTPError(500, "Invalid operation performed.")

        if not self._instance._id:
            db.Project.insert_one(self._instance)
        else:
            db.Project.update_one(self._instance)
