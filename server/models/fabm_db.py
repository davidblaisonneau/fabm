#~ 
db.define_table(
    'machines',
    Field('machine_id', 'string', notnull=True),
    Field('machine_description', 'list:string', notnull=True),
    Field('place', 'string', notnull=True),
    Field('pictures', 'list:reference pictures'),
    Field('status', 'string', notnull=True),
    Field('required_badges', 'list:reference badges'),
    Field('usages', 'list:reference usages'),
    Field('reservation_list', 'list:reference reservations'),
    Field('events', 'list:reference events'),
    Field('consumables', 'list:reference consumables'),
    Field('price_per_unit', 'float'),
    Field('unit_type', 'string'),
    format = '%(machine_id)s')

db.define_table(
    'pictures',
    Field('pictures', 'upload', uploadfolder=os.path.join(request.folder,'static/pictures'), notnull=True))

db.define_table(
    'reservations',
    Field('start_date', 'datetime', notnull=True),
    Field('stop_date', 'datetime', notnull=True),
    Field('user_id', 'reference auth_user', notnull=True,  default=auth.user.id),
    Field('validated_by', 'reference auth_user'),
    Field('events', 'list:reference events'),
    Field('machine', 'reference machines'),
    format = '%(machine)s %(start_date)s/$(stop_date)s')
db.reservations.validated_by.requires=IS_IN_DB(db(db.auth_membership.group_id==1))

db.define_table(
    'usages',
    Field('machine', 'reference machines', notnull=True),
    Field('usage_date', 'datetime', default=request.now),
    Field('usage_message', 'string', notnull=True),
    Field('price', 'float', notnull=True),
    Field('user_id', 'reference auth_user', notnull=True),
    Field('fabmanager', 'reference auth_user'),
    Field('details', 'json'),
    format = '%(machine)s %(date)s')

db.define_table(
    'events',
    Field('event_date', 'datetime', default=request.now),
    Field('event_message', 'string', notnull=True),
    Field('event_type',  requires = IS_IN_SET(['log', 'message']), default='log', notnull=True),
    Field('user_id', 'reference auth_user',  default=auth.user.id),
    format = '%(event_date)s [%(id)s]')

db.define_table(
    'consumables',
    Field('name', 'string', notnull=True),
    Field('quantity', 'integer', notnull=True),
    Field('consumable_location', 'string'),
    Field('events', 'list:reference events'),
    format = '%(name)s')

db.define_table(
    'badges',
    Field('badge_type', 'string', notnull=True),
    Field('badge_level',  notnull=True, requires = IS_IN_SET(['super user', 'operator', 'administrator'])),
    Field('icon', 'upload',  notnull=True, uploadfolder=os.path.join(request.folder,'static/badges')),
    format = '%(badge_type)/%(badge_level)')
