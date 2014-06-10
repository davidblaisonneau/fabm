#!/usr/bin/python

exclude=['']
import os
import glob
import sys
sys.path.append("/home/david/Documents/Dev/web2py")
from gluon import *
db = DAL('sqlite://storage.sqlite', folder='/home/david/Documents/Dev/web2py/applications/fabm/databases', auto_import=True)

def delete():
    for tablename in db.tables[:]:
        if tablename in exclude or tablename[0:4]=="auth":
            print("keep "+tablename)
        else:
            table=db[tablename]
            try:
                print("delete "+tablename)
                filelist=glob.glob("/home/david/Documents/Dev/web2py/applications/fabm/databases/*"+tablename+".table")
                if len(filelist)>0: os.remove(filelist[0])
                table.drop()
            except:
                print("failed to delete "+tablename)
                print(sys.exc_info())
    db.commit()
delete() 
