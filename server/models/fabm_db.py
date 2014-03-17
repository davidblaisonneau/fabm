import hashlib
import random

#~ Set requires on fabmanagers lists
rows = db(db.auth_membership.group_id==1).select(db.auth_membership.id,db.auth_membership.user_id)
managers=[]
for i in range(0,len(rows)): managers.append(rows.render(i))

db.define_table(
    'machines',
    Field('name', 'string', notnull=True),
    Field('machine_description', 'list:string', notnull=True),
    Field('machine_id', 'string', writable=False, default=hashlib.sha224( str(random.getrandbits(256)) ).hexdigest()),
    Field('place', 'string', notnull=True),
    Field('pictures', 'list:reference pictures'),
    Field('status', 'string', notnull=True),
    Field('required_badges', 'list:reference badges'),
    Field('usages', 'list:reference usages', writable=False),
    Field('reservations', 'list:reference reservations'),
    Field('events', 'list:reference events',writable=False),
    Field('consumables', 'list:reference consumables'),
    Field('price_per_unit', 'float'),
    Field('unit_type' ),
    format = '%(name)s')
db.machines.pictures.requires = IS_IN_DB(db,'pictures.id','%(name)s',multiple=True)
db.machines.required_badges.requires = IS_IN_DB(db,'badges.id','%(badge_type)s/%(badge_level)s',multiple=True)
db.machines.usages.requires = IS_IN_DB(db,'usages.id','%(machine)s %(date)s',multiple=True)
db.machines.reservations.requires = IS_IN_DB(db,'reservations.id','%(machine)s %(start_date)s/$(stop_date)s',multiple=True)
db.machines.consumables.requires=IS_IN_DB(db,'consumables.id','%(name)s',multiple=True)
db.machines.unit_type.requires = IS_IN_SET(['minute', 'cm3', 'gramme'])
db.machines.unit_type.default='minute'
db.machines.status.requires = IS_IN_SET(['available', 'maintenance', 'broken',])
db.machines.status.default='available'

db.define_table(
    'categories',
    Field('name', 'string', notnull=True),
    format = '%(name)s')
    
db.define_table(
    'pictures',
    Field('name', 'string', notnull=True),
    Field('category', 'reference categories'),
    Field('picture', 'upload', uploadfolder=os.path.join(request.folder,'static/pictures'), notnull=True,autodelete=True),
    Field('thumb','upload', uploadfolder=os.path.join(request.folder,'static/pictures'),writable=False,readable=True,autodelete=True),
    format = '%(name)s')
db.pictures.thumb.represent = lambda value,row: IMG(_src=URL('default','download', args=value),_width=50)
db.pictures.category.requires=IS_IN_DB(db,'categories.id','%(name)s')

db.define_table(
    'reservations',
    Field('start_date', 'datetime', notnull=True),
    Field('stop_date', 'datetime', notnull=True),
    Field('user_id', 'reference auth_user', notnull=True),
    Field('validated_by', 'reference auth_user'),
    Field('events', 'list:reference events',writable=False),
    Field('machine', 'reference machines'),
    format = '%(machine)s %(start_date)s/$(stop_date)s')
db.reservations.machine.requires=IS_IN_DB(db,'machines.id')
db.reservations.user_id.requires=IS_IN_DB(db,'auth_user.id','%(first_name)s %(last_name)s')
db.reservations.events.requires=IS_IN_DB(db,'events.id',multiple=True)
db.reservations.validated_by.requires=IS_IN_SET([r['id'] for r in managers], labels=[r['user_id'] for r in managers])

db.define_table(
    'usages',
    Field('machine', 'reference machines', notnull=True),
    Field('usage_date', 'datetime', default=request.now),
    Field('usage_message', 'string', notnull=True),
    Field('price', 'float', notnull=True),
    Field('user_id', 'reference auth_user'),
    Field('fabmanager', 'reference auth_user'),
    Field('details', 'json'),
    format = '%(machine)s %(date)s')
db.usages.machine.requires=IS_IN_DB(db,'machines.id')
db.usages.user_id.requires=IS_IN_DB(db,'auth_user.id','%(first_name)s %(last_name)s')
db.usages.fabmanager.requires=IS_IN_SET([r['id'] for r in managers], labels=[r['user_id'] for r in managers])

db.define_table(
    'events',
    Field('event_date', 'datetime', default=request.now),
    Field('event_message', 'string', notnull=True),
    Field('event_type',  requires = IS_IN_SET(['log', 'message']), default='log', notnull=True),
    Field('user_id', 'reference auth_user'),
    format = '%(event_date)s [%(id)s]')
db.events.user_id.requires=IS_IN_DB(db,'auth_user.id','%(first_name)s %(last_name)s')

db.define_table(
    'consumables',
    Field('name', 'string', notnull=True),
    Field('quantity', 'integer', notnull=True),
    Field('consumable_location', 'string'),
    Field('events', 'list:reference events',writable=False),
    Field('pictures', 'reference pictures'),
    format = '%(name)s')
db.consumables.events.requires=IS_IN_DB(db,'events.id',multiple=True)
db.consumables.pictures.requires = IS_IN_DB(db,'pictures.id','%(name)s')

db.define_table(
    'badges',
    Field('badge_type', 'string', notnull=True),
    Field('badge_level',  notnull=True, requires = IS_IN_SET(['super user', 'operator', 'administrator'])),
    Field('icon', 'upload',  notnull=True, uploadfolder=os.path.join(request.folder,'static/badges'),autodelete=True),
    format = '%(badge_type)s/%(badge_level)s')


#~ Set default user
if auth.user!=None:
    db.events.user_id.default = auth.user.id
    db.reservations.user_id.default = auth.user.id
    db.usages.fabmanager.default = auth.user.id
    
