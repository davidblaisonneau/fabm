from gluon import current
from fabuser import Fabuser
from event import Event

def index():
    fabuser = Fabuser(db,auth)
    user = fabuser.get_user(13)
    res = fabuser.set_fabmanager(True)
    return dict(fabuser=res)
    
def create():
    res = db.auth_user.insert(
            first_name = "aaa",
            last_name = "aaa",
            email = "aaa@aaa.aaa",
            password = "aaa",
            user_id = user_id,
        )
    return dict(res=res)
    
def delete():
    res = db((db.auth_user.id=='')).delete()
    return dict(res=res)

def test():
    a = db.tag.insert(name='red')
    b = db.tag.insert(name='yellow')
    c = db.tag.insert(name='green')
    db.product.insert(name='Toy Car',tags=[a, b])
    products = db(db.product.tags.contains(b)).select().first()
    products.tags.append(c)
    products.update_record()
    return dict(products=products,tags=products.tags)
