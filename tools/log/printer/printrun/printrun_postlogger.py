import re
import sys
import httplib, urllib
import json
import datetime
import pprint
import logging
import errno
from socket import error as socket_error

#~ Params
logFile = 'log.txt'
ws={}
ws['server']= "localhost:8888"
ws['url']= "/usage/push/printer"

#~ Prepare log
logging.basicConfig(filename=logFile,level=logging.INFO)
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
stats['date'] = str(datetime.datetime.now())
stats['tool'] = sys.argv[1]
stats['duration'] = int(sys.argv[2])
stats['object'] = {}
stats['material quantity'] = 0

#~ Check if it is an error or not
if stats['duration'] < 0:
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
                print 'no matches found'
            else:
                if re.search('^; generated', line):
                    stats['object']['gcode-generation']=line.strip("\n; ")
                elif re.search('=', line):
                    match = pattern.match(line)
                    stats['object'][match.group(1)]=match.group(2)
                    if match.group(3) and match.group(1) == 'filament used':
                        stats['material quantity']=match.group(4)
    logging.debug('GCode parsed')
    logging.info(pprint.pformat(stats))

#~ Send data to HTTP WebService
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
try:
    conn = httplib.HTTPConnection(ws['server'])
    conn.request("POST", ws['url'], json.dumps(stats), headers)
    logging.info('Data sent to '+ws['server']+ws['url'])
    response = conn.getresponse()
    if response.status == 200:
        logging.info('Server response: OK')
    else:
        logging.error('Server error: '+str(response))
except (httplib.HTTPException, socket_error) as ex: 
    logging.error('Error received: '+str(ex))



