#~ from pymongo import MongoClient
#~ from bson import json_util
#~ import json

@request.restful()
def usage():
    def GET(id):
        usages = SQLTABLE(db(db.usage.id==id).select(),
            columns=["usage.date",
                    "usage.duration",
                    "usage.result",
                    "usage.logType",
                    "usage.tool",
                    "usage.object",],
            headers={"usage.date": "Date",
                    "usage.duration": "Durée",
                    "usage.object": "Objet",
                    "usage.logType": "Type",
                    "usage.tool": "Machine",
                    "usage.result": "Résultat"})
        return dict(usages=usages)
        #~ return db['usage'].
        #~ usage_list = usage.find().sort([('date',-1)]).limit(100)
        #~ return dict(message=BEAUTIFY(list(usage_list)))
        
    #~ def POST(*args,**vars):
        #~ usage_data_json = json.loads(self.request.body, object_hook=json_util.object_hook)
        #~ usage_id = usage.insert(usage_data_json)
        #~ return_ok
        #~ 
    #~ def PUT(*args,**vars):
        #~ return dict(message=BEAUTIFY(request))
    #~ 
    #~ def DELETE(*args,**vars):
        #~ return dict(message=BEAUTIFY(request))
        
    return dict(GET=GET,
                #~ POST=POST,
                #~ PUT=PUT,
                #~ DELETE=DELETE,
                )
