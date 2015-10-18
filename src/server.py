import os
import sys
import tempfile
import imghdr
import multiprocessing
import urllib2

import numpy

import cherrypy
import PIL.Image
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


sys.path.append("restpoints/flowerrecognition")

sys.path.append("../config")
import config


###################     Helpers       ################

def _prepare_local_file_from_stream(mediafile):
    if not _valid_upload(mediafile):
        raise IOError("[SERVER] Medium could not be opened!")
    # save upload temporarily
    fd, mediapath = tempfile.mkstemp()
    while True:
        data = mediafile.file.read(8192)
        if not data:
            break
        os.write(fd, data)
    os.close(fd)
    return mediapath


def _valid_upload(mediafile):
    if mediafile.file.closed:
        print >> sys.stderr, "[SERVER] Upload seems to be corrupt: " + mediafile.filename
        return False
    return True


def _valid_image(imagepath):
    if imghdr.what(imagepath) is None:
        try:
            Image.open(imagepath)
        except IOError:
            print >> sys.stderr, "[SERVER] Image has wrong format: " + str(imagepath)
            return False
    return True


def _safe_remove(path):
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except Exception, err:
            print >> sys.stderr, "[SERVER] Could not remove file: " + path
            print >> sys.stderr, err


def _REST_callback(callback, jobid, result):
    post_data = {"result": result,
                 "jobid": jobid}
    print "[SERVER] REST Callback %s (jobid=%s):" % (callback, jobid)
    try:
        datagen, headers = multipart_encode(post_data)
        req = urllib2.Request(callback, datagen, headers)
        result = urllib2.urlopen(req)
        result_str = result.read()
        print "[SERVER] Callback successful (jobid=%s). Got response: %s\n\n" % (jobid,
                                                                   result_str)
    except Exception as e:
        print "[SERVER] WARNING - Callback failed (jobid=%s).\n\n" % jobid
        print e


def _run_flowerrecognition(toexecute_job, flowerrecognition, executed_jobs):
    input_fn = toexecute_job["mediapath"]
    result = flowerrecognition.run(input_fn)
    print result
    _REST_callback("http://" + config.BACKEND_IP + ":" + str(config.BACKEND_PORT) + "/setasfinished", toexecute_job["jobid"], result)
    _safe_remove(input_fn)


def _caffe_worker(toexecute_jobs, executed_jobs):
    from flowerrecognition import FlowerRecognition
    flowerrecognition = FlowerRecognition()

    register_openers()

    while True:
        toexecute_job = toexecute_jobs.get()
        if toexecute_job["restpoint"] == "flowerrecognition":
            _run_flowerrecognition(toexecute_job, flowerrecognition, executed_jobs)


###################     ServerREST       ################


class ServerREST(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.toexecute_jobs = multiprocessing.Queue()
        self.executed_jobs = multiprocessing.Queue()
        self.finished_jobs = {}
        self._caffe_worker_process = multiprocessing.Process(target=_caffe_worker,
                                             args=(self.toexecute_jobs,
                                                   self.executed_jobs))
        self._caffe_worker_process.daemon = True
        self._caffe_worker_process.start()

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
        msg += "provides a REST interface to the ML  back-end."
        msg += "\n<br>\n<br>\n"
        msg += "Try e.g. /apply to apply the module to an image or video! "
        msg += "\n<br>\n<br>\n"
        msg += "For more information check out the DeepDream  "
        msg += "documentation or contact: fierarufmihai@gmail.com"
        return msg


    @cherrypy.expose
    def flowerrecognition(self, jobid, mediafile):
        mediapath = _prepare_local_file_from_stream(mediafile)
        if not _valid_image(mediapath):
            _safe_remove(mediapath)
            return "Mediafile not an image"

        toexecute_job = {"jobid": jobid,
               "restpoint": "flowerrecognition",
               "mediapath": mediapath}

        self.toexecute_jobs.put(toexecute_job)

    @cherrypy.expose
    def setasfinished(self, jobid, result):
        self.finished_jobs[jobid] = result

    @cherrypy.expose
    def checkfinished(self, jobid):
        if jobid in self.finished_jobs:
            toreturn = self.finished_jobs[jobid]
            del self.finished_jobs[jobid]
        else:
            toreturn = "0"
        return toreturn


###################     Main       ################

if __name__ == '__main__':
    server = ServerREST(config.BACKEND_IP, config.BACKEND_PORT)
    server.start()







