#!/usr/bin/python

import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, tornado.httputil
import os.path, random, string
from bson import json_util
import json
import pprint
from pymongo import MongoClient
import logging
import datetime

#~ Parameters
serverPort = 8888
logFile = 'server.log'

#~ Prepare log
logging.basicConfig(filename=logFile,level=logging.INFO)

#~ Mongo Database
client = MongoClient()
db = client.fablab
usage = db.usage

#~ URL router
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", UploadHandler),
            (r"/ws/usage/(.*)", FabMUsage),
            (r"/angularjs/(.*)",tornado.web.StaticFileHandler, {"path": "./angularjs"},),
            (r"/static/(.*)",tornado.web.StaticFileHandler, {"path": "./static"},),
            (r"/lib/(.*)",tornado.web.StaticFileHandler, {"path": "./lib"},),
            (r"/img/(.*)",tornado.web.StaticFileHandler, {"path": "./img"},),
            (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": "./js"}),
            (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": "./css"}),
        ]
        tornado.web.Application.__init__(self, handlers)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("form.html")

class FabMUsage(tornado.web.RequestHandler):
    def post(self):
        usage_data_json = json.loads(self.request.body, object_hook=json_util.object_hook)
        usage_id = usage.insert(usage_data_json)
        logging.info('new usage')
        logging.info(pprint.pformat(usage_data_json))
    def get(self):
        #~ print "**** URI = "+self.request.uri
        usage_list = usage.find().sort([('date',-1)]).limit(100)
        self.write(json.dumps(list(usage_list), default=json_util.default))

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        args= {}
        files = {}
        boundary = self.request.headers['Content-Type'].split('=')[1]
        tornado.httputil.parse_multipart_form_data(
            boundary,
            self.request.body,
            args,
            files)
        #~ print files
        for upfiles in files['files[]']:
            print "Receive file "+upfiles.filename
            newFile = open ("./files/" + upfiles.filename, "wb")
            newFile.write(upfiles.body)
            newFile.close()
        #~ file1 = self.request.files['file1'][0]
        #~ original_fname = file1['filename']
        #~ extension = os.path.splitext(original_fname)[1]
        #~ fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        #~ final_filename= fname+extension
        #~ output_file = open("uploads/" + final_filename, 'w')
        #~ output_file.write(file1['body'])
        #~ self.finish("file" + final_filename + " is uploaded")
    def get(self):
        print self.request

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(serverPort)
    logging.info('----------------------------------------')
    logging.info('Server loaded - '+ str(datetime.datetime.now()))
    print "FabM server - https://github.com/davidblaisonneau/fabm"
    print "------------------------------------------------------"
    print "server started on port: "+str(serverPort)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
