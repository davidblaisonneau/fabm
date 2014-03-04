#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gluon import current
from gluon.dal import DAL, Field
from gluon.sqlhtml import SQLFORM

class Fabuser(object):
    """Build a User object"""
    
    def __init__(self,
                    auth_user = current.db.auth_user,
                    auth_membership = current.db.auth_membership,
                    auth = current.auth):
        self.auth_user = auth_user
        self.auth_membership = auth_membership
        self.request = current.request
        self.session = current.session
        self.auth = auth
        self.user_id = None
        self.user = None
        
    def get_grid(self):
        self.auth_user.badges.writable=True
        self.auth_user.UM_balance.writable=True
        self.auth_user.member_end_date.writable=True
        self.auth_user._singular = "User"
        self.auth_user._plural = "Users"
        grid = SQLFORM.smartgrid(self.auth_user,
                                linked_tables=['badges',],
                                searchable= dict(parent=True, child=True),
                                create=False, 
                                editable = self.auth.has_membership(role='Fab Manager'),
                                deletable = self.auth.has_membership(role='Fab Manager'),
                                showbuttontext=False,
                                )
        return dict(grid=grid)
        
    def get_user(self,user_id):
        if user_id==None:
            return None
        else:
            self.user = self.auth_user(self.auth_user.id==user_id)
            if self.user !=None:
                self.user_id = user_id
            return self.user
        
    #~ def set_fabmanager(enable=false):
        
        
        
    #~ def delete():
