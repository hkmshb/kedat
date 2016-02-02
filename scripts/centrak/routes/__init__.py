"""
Routes (Controller) packages.
"""
import os
from cork import Cork



__all__ = ['admin', 'account', 'api', 'core']
_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'auth_conf'))


# authnz
authnz = Cork(_path)
authorize = authnz.make_auth_decorator(fail_redirect="/login", role="user")
