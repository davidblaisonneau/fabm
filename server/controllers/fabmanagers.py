from event import Event
current.auth = auth
from fabuser import Fabuser

response.menu = [[T('Users'), False, URL('users')],
                 [T('Machines'), False, URL('machines')],
                 [T('Consumables'), False, URL('consumables2')],
                 [T('Usages'), False, URL('usages')],
                 [T('Reservations'), False, URL('reservations')],
                 [T('Categories'), False, URL('categories')],
                 [T('Badges'), False, URL('badges3')],
                 [T('Pictures'), False, URL('pictures')],
                 [T('Logs'), False, URL('logs')]]


@auth.requires(auth.has_membership(role='Fab Manager'))
def index():
    response.flash = T("You are a FabManager :)")
    return dict()
    
@auth.requires(auth.has_membership(role='Fab Manager'))
def users():
    fabuser = Fabuser(db,auth)
    return fabuser.get_grid()

@auth.requires(auth.has_membership(role='Fab Manager'))
def machines():
    db.machines._singular = "Machine"
    db.machines._plural = "Machines"
    grid = SQLFORM.smartgrid(db.machines,
                                linked_tables=['usages','pictures','badges','reservations','events','consumables',],
                                searchable= dict(parent=True, child=True),
                                editable = auth.has_membership(role='Fab Manager'),
                                deletable = auth.has_membership(role='Fab Manager'),
                                showbuttontext=False,
                            )
    return locals()

@auth.requires(auth.has_membership(role='Fab Manager'))
def usages():
    db.usages._singular = "Usage"
    db.usages._plural = "Usages"
    grid = SQLFORM.smartgrid(db.usages,
                                linked_tables=['auth_user','machines',],
                                searchable= dict(parent=True, child=True),
                                create=False, 
                                editable = auth.has_membership(role='Fab Manager'),
                                deletable = auth.has_membership(role='Fab Manager'),
                                showbuttontext=False,
                            )
    return locals()

@auth.requires(auth.has_membership(role='Fab Manager'))
def reservations():
    db.reservations._singular = "Reservations"
    db.reservations._plural = "Réservations"
    grid = SQLFORM.smartgrid(db.reservations,
                                linked_tables=['auth_user','event','machines',],
                                searchable= dict(parent=True, child=True),
                                create=True, 
                                editable = auth.has_membership(role='Fab Manager'),
                                deletable = auth.has_membership(role='Fab Manager'),
                                showbuttontext=False,
                            )
    return locals()
    
@auth.requires(auth.has_membership(role='Fab Manager'))
def logs():
    event = Event(db)
    return dict(form=event.get_grid())

@auth.requires(auth.has_membership(role='Fab Manager'))
def categories():
    db.categories.id.readable=False
    query=((db.categories))
    fields = (db.categories.id, db.categories.name)
    
    headers = {'categories.id':   'ID',
           'categories.name': 'Type', }
           
    default_sort_order=[db.categories.id]
    form = SQLFORM.grid(query=query, fields=fields, headers=headers, orderby=default_sort_order,
            create=True, deletable=True, editable=True, maxtextlength=32, paginate=25,showbuttontext=False)
    return dict(form=form)

@auth.requires(auth.has_membership(role='Fab Manager'))
def consumables():
    
    db.consumables.events.writable=False
    db.consumables._singular = "Consumable"
    db.consumables._plural = "Consumables"
    grid = SQLFORM.smartgrid(db.consumables,
                                linked_tables=['events'],
                                searchable= dict(parent=True, child=True),
                                editable = auth.has_membership(role='Fab Manager'),
                                deletable = auth.has_membership(role='Fab Manager'),
                                showbuttontext=False,
                            )
    return locals()


@auth.requires(auth.has_membership(role='Fab Manager'))
def consumables2():

    query=((db.consumables))
    fields = (db.consumables.name, db.consumables.quantity, db.consumables.consumable_location, db.consumables.category,db.consumables.price, db.consumables.picture, db.consumables.thumb)
    headers = {'consumables.name':   'Name',
                'consumables.quantity': 'quantity',
                'consumables.consumable_location': 'location',
                'consumables.category': 'category',
                'consumables.price': 'price',
                'consumables.thumb': 'thumbnail',
                'consumables.picture': 'picture',
                 }
    default_sort_order=[db.consumables.category]
    form = SQLFORM.grid(
            query=query,
            fields=fields,
            headers=headers,
            orderby=default_sort_order,
            create=True,
            deletable=True,
            editable=True,
            paginate=25,
            showbuttontext=False,
            upload=URL('default','download'),
            maxtextlength=64,
            oncreate=makeConsThumbnail,
            onupdate=makeConsThumbnail,
            )
    resize=False
    if len(request.args)>1 and (request.args(0) in 'new' or 'edit'):
        db.consumables.thumb.readable = False
    return dict(form=form)

@auth.requires(auth.has_membership(role='Fab Manager'))
def badges():
    db.badges.id.readable=False
    query=((db.badges))
    fields = (db.badges.id, db.badges.category, db.badges.lvl, db.badges.picture)
    
    headers = {'badges.id':   'ID',
           'badges.category': 'Type',
           'badges.lvl': 'Level',
           'badges.picture': 'Icon' }
           
    default_sort_order=[db.badges.id]
    form = SQLFORM.grid(query=query, fields=fields, headers=headers, orderby=default_sort_order,
            create=True, deletable=True, editable=True, maxtextlength=32, paginate=25,showbuttontext=False)
    return dict(form=form)

@auth.requires(auth.has_membership(role='Fab Manager'))
def badges2():
    filter = db.badges.id==request.args[0] if len(request.args)!=0 else db.badges
    badges = db(filter).select()
    form = SQLFORM(filter).process()
    if form.accepted:
        response.flash = TABLE(TR(
                            TD(IMG(_src="/fabm/static/badges/"+form.vars.icon, _width="100px")),
                            TD(DIV(form.vars.category),DIV(T(form.vars.lvl)),DIV("inserted"))))
    return dict(badges=badges,form=form,args=request.args)

@auth.requires(auth.has_membership(role='Fab Manager'))
def badges3():
    query=((db.badges))
    fields = (db.badges.id, db.badges.category, db.badges.lvl, db.badges.thumb, db.badges.picture)
    headers = {'badges.id':   'ID',
                'badges.category': 'category',
                'badges.lvl': 'level',
                'badges.thumb': 'thumbnail',
                'badges.picture': 'picture',
                 }
    default_sort_order=[db.badges.category]
    form = SQLFORM.grid(
            query=query,
            fields=fields,
            headers=headers,
            orderby=default_sort_order,
            create=True,
            deletable=True,
            editable=True,
            paginate=25,
            showbuttontext=False,
            upload=URL('default','download'),
            maxtextlength=64,
            oncreate=makeSmallBadges,
            onupdate=makeSmallBadges,
            )
    resize=False
    if len(request.args)>1 and (request.args(0) in 'new' or 'edit'):
        db.badges.thumb.readable = False
    return dict(form=form)

@auth.requires(auth.has_membership(role='Fab Manager'))
def pictures():
    query=((db.pictures))
    fields = (db.pictures.id, db.pictures.name, db.pictures.category, db.pictures.thumb, db.pictures.picture)
    headers = {'pictures.id':   'ID',
                'pictures.name': 'name',
                'pictures.category': 'category',
                'pictures.thumb': 'thumbnail',
                'pictures.picture': 'picture',
                 }
    default_sort_order=[db.pictures.category]
    form = SQLFORM.grid(
            query=query,
            fields=fields,
            headers=headers,
            orderby=default_sort_order,
            create=True,
            deletable=True,
            editable=True,
            paginate=25,
            showbuttontext=False,
            upload=URL('default','download'),
            maxtextlength=64,
            oncreate=makePicThumbnail,
            onupdate=makePicThumbnail,
            )
    resize=False
    if len(request.args)>1 and (request.args(0) in 'new' or 'edit'):
        db.pictures.thumb.readable = False
    return dict(form=form)

def makePicThumbnail(form):
    import os, uuid
    from PIL import Image
    size=(150,150)
    folder='static/pictures/'
    thisImage=db(db.pictures.id==form.vars.id).select().first()
    im=Image.open(os.path.join(request.folder,folder) + thisImage.picture)
    im.thumbnail(size,Image.ANTIALIAS)
    thumbName='%s.thumb.jpg' % (uuid.uuid4())
    im.save(request.folder + folder + thumbName,'jpeg')
    thumbSteam = open(os.path.join(request.folder,folder) + thumbName, 'rb')
    db(db.pictures.id==form.vars.id).update(thumb=db.pictures.thumb.store(thumbSteam, thumbName))
    return 
    
def makeConsThumbnail(form):
    import os, uuid
    from PIL import Image
    size=(150,150)
    folder='static/consumables/'
    thisImage=db(db.consumables.id==form.vars.id).select().first()
    im=Image.open(os.path.join(request.folder,folder) + thisImage.picture)
    im.thumbnail(size,Image.ANTIALIAS)
    thumbName='%s.thumb.jpg' % (uuid.uuid4())
    im.save(request.folder + folder + thumbName,'jpeg')
    thumbSteam = open(os.path.join(request.folder,folder) + thumbName, 'rb')
    db(db.consumables.id==form.vars.id).update(thumb=db.consumables.thumb.store(thumbSteam, thumbName))
    return 
    
def makeSmallBadges(form):
    import os, uuid
    from PIL import Image
    size=(48,48)
    folder='static/badges/'
    thisImage=db(db.badges.id==form.vars.id).select().first()
    im=Image.open(os.path.join(request.folder,folder) + thisImage.picture)
    im.thumbnail(size,Image.ANTIALIAS)
    thumbName='%s.thumb.jpg' % (uuid.uuid4())
    im.save(request.folder + folder + thumbName,'jpeg')
    thumbSteam = open(os.path.join(request.folder,folder) + thumbName, 'rb')
    db(db.badges.id==form.vars.id).update(thumb=db.pictures.thumb.store(thumbSteam, thumbName))
    return 
