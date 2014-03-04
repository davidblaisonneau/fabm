from gluon import current
from fabuser import Fabuser
from event import Event

def index():
    fabuser = Fabuser(db,auth)
    user = fabuser.get_user(12)
    fabuser.set_fabmanager()
    return dict(fabuser=fabuser.user.history)
