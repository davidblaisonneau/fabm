from event import Event
current.auth = auth
from fabuser import Fabuser

response.menu = [[T('Users'), False, URL('users')],
                 [T('Machines'), False, URL('machines')],
                 [T('Consumables'), False, URL('consumables')],
                 [T('Usages'), False, URL('usages')],
                 [T('Reservations'), False, URL('reservations')],
                 [T('Categories'), False, URL('categories')],
                 [T('Badges'), False, URL('badges')],
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
def badges():
    db.badges.id.readable=False
    query=((db.badges))
    fields = (db.badges.id, db.badges.badge_type, db.badges.badge_level, db.badges.icon)
    
    headers = {'badges.id':   'ID',
           'badges.badge_type': 'Type',
           'badges.badge_level': 'Level',
           'badges.icon': 'Icon' }
           
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
                            TD(DIV(form.vars.badge_type),DIV(T(form.vars.badge_level)),DIV("inserted"))))
    return dict(badges=badges,form=form,args=request.args)
    
@auth.requires(auth.has_membership(role='Fab Manager'))
def pictures2():
    record = db.pictures(request.args(0))
    buttons = [TAG.button(T('Submit'),_type="submit")]
    
    if len(request.args)!=0:
        pictures = []
        buttons[:0] = [TAG.button('Back',_type="button",_onClick = "parent.location='%s'" % URL())]
        form_title=T("Modify a picture")
    else:
        pictures = db(db.pictures).select()
        form_title=T("Add a picture")

    form = SQLFORM(db.pictures, record,
                    buttons = buttons,
                    deletable=True,
                    upload=URL('default','download'),
                    )
    if form.process().accepted:
        response.flash = T('form accepted')
        redirect(URL())
    elif form.errors:
        response.flash = T('form has errors')
    return dict(pictures=pictures,form=form,form_title=form_title)

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
            oncreate=makeThumbnail,
            onupdate=makeThumbnail,
            )
    resize=False
    if len(request.args)>1 and (request.args(0) in 'new' or 'edit'):
        db.pictures.thumb.readable = False
    return dict(form=form)

def makeThumbnail(form):
    print form.vars
    size=(150,150)
    folder='static/pictures/'
    thisImage=db(db.pictures.id==form.vars.id).select()[0]
    import os, uuid
    from PIL import Image
    print thisImage
    im=Image.open(os.path.join(request.folder,folder) + thisImage.picture)
    im.thumbnail(size,Image.ANTIALIAS)
    thumbName='%s.thumb.jpg' % (uuid.uuid4())
    im.save(request.folder + folder + thumbName,'jpeg')
    thisImage.update_record(thumb=thumbName)
    return 
