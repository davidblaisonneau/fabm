from gluon import current
current.auth = auth
from fabuser import Fabuser

def index():
    fabuser = Fabuser()
    fabuser.get_user(1)
    return dict(fabuser.auth_user)
