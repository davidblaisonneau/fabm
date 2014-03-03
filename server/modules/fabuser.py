#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gluon import current
from gluon.dal import DAL, Field
from gluon.sqlhtml import SQLFORM

class Fabuser(object):
    """Build a User object"""
    
    def __init__(self,db_user,db_membership,auth):
        self.user = db_user
        self.membership = db_membership
        self.request = current.request
        self.session = current.session
        self.auth = auth
        
    def get_grid(self):
        self.user.badges.writable=True
        self.user.UM_balance.writable=True
        self.user.member_end_date.writable=True
        self.user._singular = "User"
        self.user._plural = "Users"
        grid = SQLFORM.smartgrid(self.user,
                                linked_tables=['badges',],
                                searchable= dict(parent=True, child=True),
                                create=False, 
                                editable = self.auth.has_membership(role='Fab Manager'),
                                deletable = self.auth.has_membership(role='Fab Manager'),
                                showbuttontext=False,
                                )
        return dict(grid=grid)
