"""
Routes and views for admin access.
"""
from bottle import HTTPError, route, request, redirect
import pymongo

from kedat.core import Storage as _
from utils import view, get_session
import db, forms



@route('/admin/')
@view('admin/index')
def index():
    return {
        'title': 'Admin',
        'stat': _({
            'count_xforms': db.XForm.count(),
            'count_projects': db.Project.count()
        })
    }




@route('/admin/xforms/')
@view('admin/xforms')
def xforms():
    forms = db.XForm.get_all(include_inactive=True)
    return { 'title':'XForms', 'records': forms }


@route('/admin/projects/')
@view('admin/projects')
def projects():
    def func(xforms):
        def f(id):
            for xf in xforms:
                if xf.id_string == id:
                    return xf.title
            return ''
        return f

    projects = db.Project.get_all(include_inactive=True)
    xforms = db.XForm.get_all(include_inactive=True)
    return {
        'title': 'Projects', 'records': projects,
        'get_xform_title': func(xforms),
    }


@route('/admin/projects/create', method=['GET', 'POST'])
@route('/admin/projects/<id>/', method=['GET', 'POST'])
@view('admin/project-form')
def manage_project(id=None):
    project = _(xforms=[]) if not id else db.Project.get_by_id(id)
    if not project:
        raise HTTPError(404, "Project not found: %s" % id)

    xforms = db.XForm.get_all_unassigned(False, False)
    session = get_session()
        
    if request.method == 'POST':
        form = forms.ProjectForm(request)
        try:
            if form.is_valid():
                form.save()
                action = ('created' if not id else 'updated')
                session['messages']['pass'].append('Project %s' % action)
            else:
                session['messages']['fail'].extend(form.errors)

            return redirect('/admin/projects/')
        except pymongo.errors.DuplicateKeyError:
            session['messages']['fail'].append("Provided Project Id and/or Name already exists.")
            project = form._instance

    return {
        'title':'Projects',
        'project': project,
        'xforms': xforms 
    }