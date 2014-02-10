import datetime
import time
import json
from bson import json_util
from bson.objectid import ObjectId
import re

def list2imbricatedHash(l,value):
    h = dict()
    e = l.pop(0)
    if(len(l) == 0):
        h[e] = value
    else:
         h[e] = list2imbricatedHash(l,value)
    return h

#~ date2Datetime (dict)
#~      return a dict where date is translated to datetime
def date2Datetime(dic,field='date'):
    if dic.has_key(field):
        #~ We have an epoch
        if re.match('^\d+\.?\d*$',str(dic[field])):
            dic[field] = datetime.datetime.fromtimestamp(dic[field])
        elif re.match('^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.?.*$',dic[field]):
            dic[field] = datetime.datetime.strptime(dic[field].split('.')[0], "%Y-%m-%d %H:%M:%S")
    return dic
    
def serializeMongo(rows):
    #~ Recursive parse
    if type(rows) is list:
        ret_rows=[]
        for row in rows:
            ret_rows.append(serializeMongo(row))
        return ret_rows
    else :
        #~ Set ObjectId to str
        if rows.has_key('_id'):
            rows['_id'] = str(rows['_id'])
        return rows

def dateRangeSetForMongo(dic):
    return dic
  
def parseVars(data):
    if type(data) is dict:
        data = date2Datetime(data)
        if dic.has_key('start') and dic.has_key('end') :
            dic=date2Datetime(dic,'start')
            dic=date2Datetime(dic,'end')
            dic['date']={'$gte':dic['start'],'$lte':dic['end']}
            dic.pop("start", None)
            dic.pop("end", None)
        #~ for k,v in data.items():
            #~ if re.search("^int\((\d+)\)",v)
    return data
    

@request.restful()
def usage():
    mc_usage = mdb.usage
    def GET(*args,**vars):
        #~ transform vars
        
        try: vars=parseVars(vars)
        except: raise HTTP(400, "Error, probably wrong date")
        #~ If we have arguments, we require sub items, the id is the first argument
        if len(args):
            usages = mc_usage.find_one({"_id": ObjectId(args[0])})
            if usages is None: raise HTTP(404,"No such usage id")
            if len(args)>1: 
                for i in range(1,len(args)):
                    usages=usages[args[i]]
        #~ Else we return items list
        else:
            usage_list = mc_usage.find(vars).sort([('date',-1)]).limit(100)
            usages = list(usage_list)
        usages = serializeMongo(usages)
        return dict(usages=usages,vars=vars)

    def POST(*args,**vars):
        try: usage_data = date2Datetime(json.loads(request.body.read(), object_hook=json_util.object_hook))
        except: raise HTTP(400, "Error, probably wrong date")
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
