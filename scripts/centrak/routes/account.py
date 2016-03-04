from bottle import HTTPError, post, route, request, redirect
from routes import authnz, authorize
from utils import view, get_session
from forms import RegisterForm

from kedat.core import Storage as _



@route('/login', method=['GET','POST'])
@view('account/login.tpl')
def login():
    if request.method == 'POST':
        session = get_session()['messages']

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username and password:
            logged_in = authnz.login(username, password)
            if logged_in:
                return redirect('/')

            session['fail'].append('Invalid username and/or password.')
        else:
            session['warn'].append('Username and password required.')
    return {'title': 'Log In'}


@route('/logout')
def logout():
    authnz.logout(success_redirect='/')


@route('/restricted')
@view('account/restricted')
def restricted():
    return {
        'title': 'Access Restricted'
    }


@route('/register', method=['GET', 'POST'])
@view('account/register.tpl')
def register():
    session = get_session()['messages']
    if request.method == 'POST':
        form = RegisterForm(request, authnz)
        if form.is_valid():
            form.save()
            session['pass'].append('Account created!')
            return redirect('/')
        else:
            session['fail'].extend(form.errors)
    else:
        form = _(username=None, email=None)
    
    return {
        'title':'Register To Use CENTrak',
        'form': _(username=form.username, email=form.email)
    }


@route('/activate/<registration_code>')
def activate_account(registration_code):
    session = get_session()['messages']
    try:
        authnz.validate_registration(registration_code)
        session['pass'].append('Account activated!')
    except Exception as ex:
        session['fail'].append("Account activation failed. Error: %s" % str(ex))
    return redirect('/')

