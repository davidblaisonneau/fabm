#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gluon import current
from gluon.dal import DAL, Field
from gluon.sqlhtml import SQLFORM


class Fabuser(object):
    """Build a User object"""
    
    def __init__(self,db,auth):
        self.db = db
        self.request = current.request
        self.session = current.session
        self.auth = auth
        self.user_id = None
        self.user = None
        self.fabmanager_group_id = None
        
    def get_grid(self):
        """Return a SQLFORM.smartgrid"""
        self.db.auth_user.badges.writable=True
        self.db.auth_user.UM_balance.writable=True
        self.db.auth_user.member_end_date.writable=True
        self.db.auth_user._singular = "User"
        self.db.auth_user._plural = "Users"
        grid = SQLFORM.smartgrid(self.db.auth_user,
                                linked_tables=['badges',],
                                searchable= dict(parent=True, child=True),
                                create=False, 
                                editable = self.auth.has_membership(role='Fab Manager'),
                                deletable = self.auth.has_membership(role='Fab Manager'),
                                showbuttontext=False,
                                )
        return dict(grid=grid)
        
    def get_user(self,user_id):
        """Load a user"""
        if user_id==None:
            return None
        else:
            #~ self.user = self.auth_user(self.auth_user.id==user_id)
            self.user = self.db(self.db.auth_user.id==user_id).select().first()
            if self.user !=None:
                self.user_id = user_id
            return self.user
            
    def set_fabmanager(self,enable=True,user_id=None):
        """set_fabmanager push the user in the fabmanager group (or not)"""
        if self.user==None:
            if self.get_user(user_id)==None:
                return "Please select user_id"
        self.get_fabmanager_group_id()
        if enable:
            """Add to FabManager group"""
            result = self.db.auth_membership.update_or_insert(user_id=self.user_id,group_id=self.fabmanager_group_id)
            self.push_event("User '"+self.user.first_name+" "+self.user.last_name+" is set in Fab Manager group :: "+str(result))
        else:
            """Remove from FabManger group"""
            result = self.db((self.db.auth_membership.user_id==self.user_id)&(self.db.auth_membership.group_id==self.fabmanager_group_id)).delete()
            self.push_event("User '"+self.user.first_name+" "+self.user.last_name+" is removed from Fab Manager group :: "+str(result))
        return result
        
    def get_fabmanager_group_id(self):
        """get_fabmanager_group_id get the Fab Manager group id"""
        self.fabmanager_group_id = self.db(self.db.auth_group.role=="Fab Manager").select().first().id
        
    def push_event(self,msg,m_type='log'):
        from event import Event
        """push_event add a event to the user"""
        if self.user==None:
            if self.get_user(user_id)==None:
                return "Please select user_id"
        event = Event(self.db)
        self.user.history=[event.add(msg,m_type)]
        self.user.update_record()
        
        
