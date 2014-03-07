#~ 

db.define_table(
    'machines',
    Field('machine_id', 'string', notnull=True),
    Field('machine_description', 'list:string', notnull=True),
    Field('place', 'string', notnull=True),
    Field('pictures', 'list:reference pictures',requires = IS_IN_DB(db,'pictures.id',multiple=True)),
    Field('status', 'string', notnull=True),
    Field('required_badges', 'list:reference badges', requires = IS_IN_DB(db,'badges.id','%(badge_type)s/%(badge_level)s',multiple=True)),
    Field('usages', 'list:reference usages'),
    Field('reservation_list', 'list:reference reservations', requires = IS_IN_DB(db,'reservations.id',multiple=True)),
    Field('events', 'list:reference events',writable=False),
    Field('consumables', 'list:reference consumables',requires=IS_IN_DB(db,'consumables.id',multiple=True)),
    Field('price_per_unit', 'float'),
    Field('unit_type', requires = IS_IN_SET(['minute', 'cm3', 'gramme']), default='minute', ),
    format = '%(machine_id)s')


db.define_table(
    'pictures',
    #~ Field('name', 'string', notnull=True),
    Field('pictures', 'upload', uploadfolder=os.path.join(request.folder,'static/pictures'), notnull=True))

db.define_table(
    'reservations',
    Field('start_date', 'datetime', notnull=True),
    Field('stop_date', 'datetime', notnull=True),
    Field('user_id', 'reference auth_user', notnull=True),
    Field('validated_by', 'reference auth_user'),
    Field('events', 'list:reference events',writable=False),
    Field('machine', 'reference machines'),
    format = '%(machine)s %(start_date)s/$(stop_date)s')

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

db.define_table(
    'events',
    Field('event_date', 'datetime', default=request.now),
    Field('event_message', 'string', notnull=True),
    Field('event_type',  requires = IS_IN_SET(['log', 'message']), default='log', notnull=True),
    Field('user_id', 'reference auth_user'),
    format = '%(event_date)s [%(id)s]')

db.define_table(
    'consumables',
    Field('name', 'string', notnull=True),
    Field('quantity', 'integer', notnull=True),
    Field('consumable_location', 'string'),
    Field('events', 'list:reference events',writable=False),
    format = '%(name)s')

db.define_table(
    'badges',
    Field('badge_type', 'string', notnull=True),
    Field('badge_level',  notnull=True, requires = IS_IN_SET(['super user', 'operator', 'administrator'])),
    Field('icon', 'upload',  notnull=True, uploadfolder=os.path.join(request.folder,'static/badges')),
    format = '%(badge_type)s/%(badge_level)s')

#~ Set requires on fabmanagers lists
rows = db(db.auth_membership.group_id==1).select(db.auth_membership.id,db.auth_membership.user_id)
managers=[]
for i in range(0,len(rows)): managers.append(rows.render(i))
db.reservations.validated_by.requires=IS_IN_SET([r['id'] for r in managers], labels=[r['user_id'] for r in managers])
db.usages.fabmanager.requires=IS_IN_SET([r['id'] for r in managers], labels=[r['user_id'] for r in managers])

#~ Set default user
if auth.user!=None:
    db.events.user_id.default = auth.user.id
    db.reservations.user_id.default = auth.user.id
    db.fabmanager.user_id.default = auth.user.id
    
