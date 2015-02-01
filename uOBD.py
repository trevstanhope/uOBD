"""
    OBD
"""
__author__ = 'Trevor Stanhope'
__version___ = 0.1

# Dependencies
import logging
import pymongo
import cherrypy
from cherrypy.process.plugins import Monitor
from cherrypy import tools
import os
from datetime import datetime

# Configuration
CONFIG = {
    "MONGO_ADDR" : "127.0.0.1",
    "MONGO_PORT" : 27017,
    "MONGO_DB" : "%Y%m",
    "CHERRYPY_ADDR" : "127.0.0.1",
    "CHERRYPY_PORT" : 8080,
    "LOG_FILE" : "%Y%m%d"
}

## Pretty Print
def pretty_print(task, msg):
    date = datetime.strftime(datetime.now(), '%d/%b/%Y:%H:%M:%S')
    print('[%s] %s %s' % (date, task, msg))

# Classes
class WatchDog:
    def __init__(self, config):
        self.config = config
        self.mongo_client = pymongo.MongoClient(config['MONGO_ADDR'], config['MONGO_PORT'])        
        self.init_logging()

    def init_db(self):
        try:
            self.mongo_client = pymongo.MongoClient(config['MONGO_ADDR'], config['MONGO_PORT'])        
            self.pretty_print('DB', 'Initializing DB')
        except Exception as error:
            self.pretty_print('DB', str(error))

    def init_logging(self):
        try:
            self.pretty_print('LOG', 'Initializing Log')
            self.log_path = '%s/%s' % (self.LOG_DIR, datetime.strftime(datetime.now(), self.LOG_FILE))
            logging.basicConfig(filename=self.log_path, level=logging.DEBUG)
        except Exception as error:
            self.pretty_print('LOG', str(error))

    """
    Handler Functions
    """
    ## Render Index
    @cherrypy.expose
    def index(self):
        html = open('static/index.html').read()
        return html
    
    ## Handle Posts
    @cherrypy.expose
    def default(self, *args, **kwargs):
        try:
            pretty_print('MSG', str(kwargs))
        except Exception as err:
            pretty_print('ERROR', str(err))
        return None
    
# Main
if __name__ == '__main__':
    daemon = WatchDog(CONFIG)
    cherrypy.server.socket_host = daemon.config['CHERRYPY_ADDR']
    cherrypy.server.socket_port = daemon.config['CHERRYPY_PORT']
    currdir = os.path.dirname(os.path.abspath(__file__))
    conf = {
        '/': {'tools.staticdir.on':True, 'tools.staticdir.dir':os.path.join(currdir,'static')},
        '/data': {'tools.staticdir.on':True, 'tools.staticdir.dir':os.path.join(currdir,'data')}, # NEED the '/' before the folder name
    }
    cherrypy.quickstart(daemon, '/', config=conf)
