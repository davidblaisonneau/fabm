#!/usr/bin/python
import re
import sys
import errno
from socket import error as socket_error
import httplib, urllib
import json
from bson import json_util
import datetime
import pprint
import logging

#~ Params
logFile = 'log.txt'
ws={}
ws['server']= "127.0.0.1:8000"
#~ ws['server']= "192.168.3.132:8000"
ws['url']= "/fabm/ws/usage.json"

#~ =====================================================================

#~ Prepare log
logging.basicConfig(filename=logFile,level=logging.INFO)
logging.info('----------------------------------------')
logging.info('New object printed')

#~ Check args
if len(sys.argv)< 4 :
    logging.error('Not enough arguments: ')
    for arg in sys.argv:
        logging.error(' * '+arg)
    exit()
else:
    logging.debug('parameters are:')
    logging.debug(' * object file: '+ sys.argv[3])
    logging.debug(' * duration: ' + sys.argv[2])
    logging.debug(' * tool: ' + sys.argv[1])

#~ Required data
stats = {}
stats['logType'] = '3Dprinter'
stats['date'] = datetime.datetime.utcnow()
stats['tool'] = sys.argv[1]

#~ Optional data
stats['object'] = {}
stats['material_quantity'] = 0
stats['duration'] = sys.argv[2]

#~ Check if it is an error or not
if stats['duration'] == "-1":
    stats['result'] = 'Error'
    stats['errorMessage'] = sys.argv[3]
    logging.info('Print failed: '+stats['errorMessage'])
else:
    stats['result'] = 'OK'
    
    #~ Specific data
    stats['object']['file'] = sys.argv[3]
    
    #~ Parse gcode data
    lines = []
    pattern = re.compile(r'^; (.+) = ([^ ]+)( \((.+)\))?\n')
    for line in open(stats['object']['file'], 'r'):
        if re.search('^;', line):
            if line == None:
                logging.error('no matches found in '+stats['object']['file'])
                print 'no matches found'
            else:
                if re.search('^; generated', line):
                    stats['object']['gcode-generation']=line.strip("\n; ")
                elif re.search('=', line):
                    match = pattern.match(line)
                    stats['object'][match.group(1).replace(' ','_')]=match.group(2)
                    if match.group(3) and match.group(1) == 'filament used':
                        stats['material_quantity']=match.group(4)
    logging.debug('GCode parsed')
    logging.info(pprint.pformat(stats))

#~ Send data to HTTP WebService
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
try:
    conn = httplib.HTTPConnection(ws['server'])
    conn.request("POST", ws['url'], json.dumps(stats, default=json_util.default), headers)
    logging.info('Data sent to '+ws['server']+ws['url'])
    response = conn.getresponse()
    print response.read()
    if response.status == 200:
        logging.info('Server response: OK')
        print "Data sent"
    else:
        logging.error('Server error: ['+str(response.status)+'] : '+response.reason)
        print "Cannot push to server, please, see logs"
except (httplib.HTTPException, socket_error) as ex: 
    logging.error('Error received: '+str(ex))
    print "Cannot push to server, please, see logs"



