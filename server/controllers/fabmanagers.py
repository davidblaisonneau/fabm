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
    
def users():
    badges = db(db.badges).select()
    users = db(db.auth_user).select()
    return dict(users=users,badges=badges)

def machines():
    machines = db(db.machines).select()
    return dict(machines=machines)

def usages():
    machines = db(db.usages).select()
    return dict(usages=usages)

def logs():
    events = db(db.events).select()
    return dict(logs=events)

def consumables():
    consumables = db(db.consumables).select()
    return dict(consumables=consumables)

def badges():
    badges = db(db.badges).select()
    form = SQLFORM(db.badges).process()
    if form.accepted:
        response.flash = TABLE(TR(
                            TD(IMG(_src="/fabm/static/badges/"+form.vars.icon, _width="100px")),
                            TD(DIV(form.vars.badge_type),DIV(T(form.vars.badge_level)),DIV("inserted"))))
        badges = db(db.badges).select()
    return dict(badges=badges,form=form)
    
def pictures():
    pictures = db(db.pictures).select()
    return dict(pictures=pictures)
