from bson import json_util
import json
        
@request.restful()
def usage():
    def GET(id = 0,val=""):
        res = db.usage if id==0 else db.usage.id==id
        if val == '':
            usages = db(res).select(orderby=~db.usage.date,limitby=(0, 10))
        else:
            usages = db(res).select(val,orderby=~db.usage.date,limitby=(0, 10))
        return dict(usages=usages)        
    def POST(*args,**vars):
        usage_data_json=json.loads(request.body.read(), object_hook=json_util.object_hook)
        usage_id = db.usage.bulk_insert([usage_data_json])
        return dict(usages=usage_id)
        
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
