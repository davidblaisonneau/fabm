from event import Event
current.auth = auth
from fabuser import Fabuser

response.menu = [[T('Users'), False, URL('users')],
                 [T('Machines'), False, URL('machines')],
                 [T('Consumables'), False, URL('consumables')],
                 [T('Usages'), False, URL('usages')],
                 [T('Badges'), False, URL('badges')],
                 [T('Pictures'), False, URL('pictures')],
                 [T('Logs'), False, URL('logs')]]


@auth.requires(auth.has_membership(role='Fab Manager'))
def index():
    response.flash = T("You are a FabManager :)")
    return dict()
    
@auth.requires(auth.has_membership(role='Fab Manager'))
def users():
    fabuser = Fabuser(db.auth_user,db.auth_membership,auth)
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
def logs():
    event = Event()
    return dict(form=event.get_grid())

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
    filter = db.badges #~.id==request.args[0] if request.args[0] else db.badge
    badges = db(filter).select()
    form = SQLFORM(filter).process()
    if form.accepted:
        response.flash = TABLE(TR(
                            TD(IMG(_src="/fabm/static/badges/"+form.vars.icon, _width="100px")),
                            TD(DIV(form.vars.badge_type),DIV(T(form.vars.badge_level)),DIV("inserted"))))
    return dict(badges=badges,form=form,args=request.args)
    
@auth.requires(auth.has_membership(role='Fab Manager'))
def pictures():
    query=((db.pictures))
    fields = (db.pictures.id, db.pictures.pictures)
    headers = {'pictures.id':   'ID',
           'pictures.pictures': 'Photo' }
    default_sort_order=[db.pictures.id]
    form = SQLFORM.grid(query=query, fields=fields, headers=headers, orderby=default_sort_order,
            create=True, deletable=True, editable=True, paginate=25,showbuttontext=False,)
    return dict(form=form)

