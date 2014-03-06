from gluon import current
from fabuser import Fabuser
from event import Event
uid = 14
def index():
    fabuser = Fabuser(db,auth)
    user = fabuser.get_user(uid)
    res = fabuser.set_fabmanager(True)
    return dict(fabuser=res)
    
def create():
    res = db.auth_user.insert(
            first_name = "aaa",
            last_name = "aaa",
            email = "aaa@aaa.aaa",
            password = "aaa",
        )
    return dict(res=res)
    
def delete():
    res = db((db.auth_user.id==uid)).delete()
    return dict(res=res)

def test():
    a = db.tag.insert(name='red')
    b = db.tag.insert(name='yellow')
    c = db.tag.insert(name='green')
    id = db.product.insert(name='Toy Car',tags=[a, b])
    product = db(db.product.id==id).select().first()
    product.tags.append(c)
    product.update_record()
    product_new = db(db.product.id==id).select().first()
    return dict(products=product_new,tags=product.tags)

def test2():
    a = db.tag.insert(name='red')
    b = db.tag.insert(name='yellow')
    c = db.tag.insert(name='green')
    e = Event(db)
    e1 = e.add('message1')
    e2 = e.add('message2')
    e3 = e.add('message3')
    id = db.product.insert(name='Toy Car',tags=[a, b])
    product = db(db.product.id==id).select().first()
    product.tags.append(c)
    if product.events==None:
        product.events=[e1,e2,e3]
    else:
        product.events.append(e1)
        product.events.append(e2)
        product.events.append(e3)
    product.update_record()
    product_new = db(db.product.id==id).select().first()
    return dict(products=product_new)

def list_fabmanagers():
    l = db(db.auth_membership.group_id==1).select(db.auth_membership.id).as_list()
    return dict(list=l.as_list())
