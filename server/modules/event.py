#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gluon import current
from gluon.dal import DAL, Field
from gluon.sqlhtml import SQLFORM


class Event(object):
    """Build an Event object"""
    
    def __init__(self,db):
        self.events = db.events
        self.request = current.request
        self.session = current.session

    def add(self,msg,m_type='log',user_id=None):
        if user_id==None and self.session.auth.user.id!=None:
            user_id = self.session.auth.user.id
        return self.events.insert(
            event_date = self.request.now,
            event_message = msg,
            event_type = m_type,
            user_id = user_id,
        )

    def get_grid(self):
        query=((self.db.events))
        fields = (self.db.events.id, self.db.events.event_date,
                    self.db.events.event_message, self.db.events.event_type,
                    self.db.events.user_id)
        headers = {'events.id':   'ID',
               'events.event_date': 'Date',
               'events.event_message': 'Message',
               'events.event_type': 'Type',
               'events.user_id': 'User' }
        default_sort_order=[self.db.events.id]
        form = SQLFORM.grid(query=query,
                            fields=fields,
                            headers=headers,
                            orderby=default_sort_order,
                            showbuttontext=False,
                            create=False, deletable=False, editable=False)
        return form

    #~ def get_mine(self,user_id=self.session.user.id):
        #~ self.events.insert(
            #~ event_date = self.request.now
            #~ event_message = message
            #~ event_type = m_type
            #~ user_id = user_id
        #~ )
