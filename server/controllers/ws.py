from bson.objectid import ObjectId
import datetime
import json
from bson import json_util

def list2imbricatedHash(l,value):
    h = dict()
    e = l.pop(0)
    if(len(l) == 0):
        h[e] = value
    else:
         h[e] = list2imbricatedHash(l,value)
    return h

def epoch2date(dic):
    if dic.has_key('epoch'):
        dic['date'] = datetime.datetime.fromtimestamp(dic['epoch'])
        dic.pop("epoch", None)
    return dic

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
        usage_data = epoch2date(json.loads(request.body.read(), object_hook=json_util.object_hook))
        if len(args):
            if len(args)>1:
                usage_data = list2imbricatedHash(list(args).pop(0),usage_data)
            usage_id = mc_usage.update({"_id": ObjectId(args[0])}, {"$set":  usage_data})
        else:
            if not usage_data.has_key('user'):
                usage_data['user']=""
            if not usage_data.has_key('fabmanager'):
                usage_data['fabmanager']=""
            usage_id = mc_usage.insert(usage_data)
        return dict(body=str(usage_id))
    return dict(GET=GET,POST=POST)
