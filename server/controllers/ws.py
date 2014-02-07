from bson.objectid import ObjectId
import bson

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
        if len(args):
            usage_data=request.body.read().decode()
            if len(args)>1:
                usage_data = list2imbricatedHash(list(args).pop(0),usage_data)
            usage_id = mc_usage.update({"_id": ObjectId(args[0])}, {"$set":  usage_data})
        else:
            usage_data_bson=request.body.read().decode()
            usage_id = mc_usage.bulk_insert([usage_data])
        return dict(body=usage_data)
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
