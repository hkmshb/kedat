from bottle import HTTPError, post, route, request, redirect
from routes import authnz, authorize
from utils import view, get_session



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

