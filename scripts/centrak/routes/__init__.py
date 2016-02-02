"""
Routes (Controller) packages.
"""
import os
from cork import Cork
from utils import make_auth_decorator


__all__ = ['admin', 'account', 'api', 'core']
_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'auth_conf'))


# authnz
authnz = Cork(_path)
authorize = make_auth_decorator(
                authnz, role='user',
                fail_unauth_redirect='/login',
                fail_auth_redirect="/restricted")
