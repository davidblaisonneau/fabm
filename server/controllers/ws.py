from bson import json_util
from bson.objectid import ObjectId
import json

def list2imbricatedHash(l,value):
    h = dict()
    e = l.pop(0)
    if(len(l) == 0):
        h[e] = value
    else:
         h[e] = list2imbricatedHash(l,value)
    return h
    
@request.restful()
def usage():
    mc_usage = mdb.usage
    def GET(*args,**vars):
        if len(args):
            usages = mc_usage.find_one({"_id": ObjectId(args[0])})
            if len(args)>1:
                for i in range(1,len(args)):
                    usages=usages[args[i]]
        else:
            usage_list = mc_usage.find().sort([('date',-1)]).limit(100)
            usages = list(usage_list)
        return dict(usages=usages)

    def POST(*args,**vars):
        msg=''
        update_data_json=''
        update_target=''
        if len(args):
            #~ usage_data_json=json.loads(request.body.read(), object_hook=json_util.object_hook)
            usage_data_json=request.body.read()
            if len(args)>1:
                args_l = list(args)
                args_l.pop(0)
                update_target = list2imbricatedHash(args_l,usage_data_json)
            usage_id = mc_usage.update({"_id": ObjectId(args[0])}, {"$set":  update_target})
        else:
            usage_data_json=json.loads(request.body.read(), object_hook=json_util.object_hook)
            usage_id = mc_usage.bulk_insert([usage_data_json])
        return dict(msg=update_target,body=usage_data_json,args=args)
    return dict(GET=GET,POST=POST)

#~ @request.restful()
#~ def usage():        
    #~ def GET(id = 0,val=""):
        #~ res = db.usage if id==0 else db.usage.id==id
        #~ if val == '':
            #~ usages = db(res).select(orderby=~db.usage.date,limitby=(0, 10))
        #~ else:
            #~ usages = db(res).select(val,orderby=~db.usage.date,limitby=(0, 10))
        #~ return dict(usages=usages)        
    #~ def POST(*args,**vars):
        #~ usage_data_json=json.loads(request.body.read(), object_hook=json_util.object_hook)
        #~ usage_id = db.usage.bulk_insert([usage_data_json])
        #~ return dict(usages=usage_id)
        #~ 
    #~ return dict(GET=GET,
                #~ POST=POST,
                #~ )
