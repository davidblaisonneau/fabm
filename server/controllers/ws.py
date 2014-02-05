from pymongo import MongoClient
from bson import json_util
import json

@request.restful()
def usage():
    def GET(id = 0):
        res = db.usage if id==0 else db.usage.id==id
        usages = db(res).select(orderby=~db.usage.date,limitby=(0, 10))
        return dict(usages=usages)
        #~ return dict(usages=usages)
        #~ return db['usage'].
        #~ usage_list = usage.find().sort([('date',-1)]).limit(100)
        #~ return dict(message=BEAUTIFY(list(usage_list)))
        
    def POST(*args,**vars):
        client = MongoClient()
        dbm = client.fablab
        #~ return dict(message=BEAUTIFY(request.body.read()))
        usage_data_json = request.body.read()
        usage_id = db.usage.bulk_insert([usage_data_json])
        return dict(usage_id=usage_id)
        
    #~ def PUT(*args,**vars):
        #~ return dict(message=BEAUTIFY(request))
    #~ 
    #~ def DELETE(*args,**vars):
        #~ return dict(message=BEAUTIFY(request))
        
    return dict(GET=GET,
                POST=POST,
                #~ PUT=PUT,
                #~ DELETE=DELETE,
                )
