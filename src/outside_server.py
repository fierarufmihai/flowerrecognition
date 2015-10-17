import os
import sys

import urllib2


import cherrypy
from poster.encode import multipart_encode

sys.path.append("restpoints/deepsentibank")
sys.path.append("restpoints/deepdream")

sys.path.append("../config")
import config


###################     Helpers       ################



def _send_request(url, post_data):
    try:
        datagen, headers = multipart_encode(post_data)
        req = urllib2.Request(url, datagen, headers)
        result = urllib2.urlopen(req)
        result_str = result.read()
    except Exception as e:
        print "[SERVER] WARNING - Request Failed"
        print e



###################     ServerREST       ################

class ServerREST(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


    def start(self):
        try:
            cherrypy.server.socket_port = self.port
            cherrypy.server.socket_host = self.ip
            cherrypy.config.update({
                'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
                'engine.autoreload_on': False
                })
            conf = {'/static': {'tools.staticdir.on': True,
                            'tools.staticdir.dir': os.path.join(os.path.dirname(__file__), "static")
                            }
            }
            cherrypy.quickstart(self, '/', config=conf)
            print "[SERVER] connected to ip %s port %s " % (self.ip, str(self.port))
        except Exception, e:
            print e


    @cherrypy.expose
    def index(self):
        msg = "This HTTP Server does not create any HTML pages, it "
        msg += "provides a REST interface to the DeepDream  back-end."
        msg += "\n<br>\n<br>\n"
        msg += "Try e.g. /apply to apply the module to an image or video! "
        msg += "\n<br>\n<br>\n"
        msg += "For more information check out the DeepDream  "
        msg += "documentation or contact: mihai . fieraru at dfki . de"
        return msg


    @cherrypy.expose
    def deepdream(self, callback, jobid, mediafile, modelname):
        url = "http://localhost:8803/deepdream"
        post_data = {"callback": callback,
               "jobid": jobid,
               "mediafile": mediafile,
               "modelname": modelname}
        _send_request(url, post_data)


    @cherrypy.expose
    def deepsentibank(self, callback, jobid, mediafile, modelname):
        url = "http://localhost:8803/deepsentibank"
        post_data = {"callback": callback,
               "jobid": jobid,
               "mediafile": mediafile,
               "modelname": modelname}
        _send_request(url, post_data)


###################     Main       ################

if __name__ == '__main__':
    server = ServerREST(config.BACKEND_IP, config.BACKEND_PORT)
    server.start()







