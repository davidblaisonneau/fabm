#!/usr/bin/python

import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, tornado.httputil
import os.path, random, string
import json
import pprint

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", UploadHandler),
            (r"/ws/usage/new", UsageNew),
            (r"/img/(.*)",tornado.web.StaticFileHandler, {"path": "./img"},),
            (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": "./js"}),
            (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": "./css"}),
        ]
        tornado.web.Application.__init__(self, handlers)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("form.html")

class UsageNew(tornado.web.RequestHandler):
    def post(self):
        print pprint.pprint(json.loads(self.request.body))

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
    http_server.listen(8888)
    print "server started"
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
