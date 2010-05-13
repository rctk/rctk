import sys
import os
import cgi

try:
    import gtk
    import gtkmozembed
except ImportError, e:
    print >> sys.stderr, "You need pygtk and gtkmozembed installed for this appserver to work"
    sys.exit(-1)

import BaseHTTPServer
import rctk

from rctk.toolkit import Toolkit

import gobject
import simplejson

basedir = os.path.dirname(rctk.__file__)

class PersistentRequestFactoryClass(object):
    def __init__(self, app):
        self.tk = Toolkit(app())

    def __call__(self, *args):
        return StandaloneHTTPServer(self.tk, *args)

class StandaloneHTTPServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, tk, *args):
        self.tk = tk
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        if self.path.startswith("/static"):
            data = open(os.path.join(basedir, self.path[1:]), "r").read()
            print >> self.wfile, data
        else: ## main.html or resources
            type, data = self.tk.serve(self.path[1:])
            self.send_response(200, "Ok")
            self.send_header("content-type", type)
            self.send_header("content-length", len(data))
            self.end_headers()

            print >> self.wfile, data

    def do_POST(self):
        method = self.path[1:]
        length = self.headers.get('content-length', -1)
        q = self.rfile.read(int(length))
        arguments = cgi.parse_qs(q)
        ## parse_qs always (?) returns lists of values, we need individual 
        ## values
        for k in arguments:
            v = arguments[k]
            if isinstance(v, list):
                arguments[k] = v[0]
        res = self.tk.handle(method, **arguments)
        res = simplejson.dumps(res)
        self.send_response(200, "Ok")
        self.send_header("content-type", "application/json")
        self.send_header("content-length", len(res))

        self.end_headers()


        print >> self.wfile, res


import socket

class StandaloneServer(object):
    ## derive from BaseHTTPServer.HTTPServer in stead?
    def __init__(self, klass):
        self.port = -1
        self.klass = klass

    def start(self):
        factory = PersistentRequestFactoryClass(self.klass)
        for i in range(31337, 31337 + 50):
            try:
                self.server = BaseHTTPServer.HTTPServer(('localhost', i), factory)
                self.port = i
                break
            except socket.error, e:
                if e.args[0] == 98: ## In use
                    continue
                raise
        if self.port != -1:
            gobject.io_add_watch(self.server.socket, gobject.IO_IN, self.handle_request)

    def handle_request(self, *a):
        self.server.handle_request()
        return True

## http://majorsilence.com/pygtk_embedded_web_browsers
class StandaloneRCTK(object): 
    """ The actual viewer. Yes, it can be that simple """
    def __init__(self, appurl):
        self.moz = gtkmozembed.MozEmbed()
                
        win = gtk.Window()
        win.set_size_request(1200, 800)
        win.add(self.moz)
        win.show_all()
        self.moz.load_url(appurl)

        ## todo: handle close window

def run(klass):
    server = StandaloneServer(klass)
    server.start()
    port = server.port
    if port == -1:
        print >> sys.stderr, "Couldn't find an available port"
        sys.exit(-1)
    s = StandaloneRCTK("http://localhost:%d/" % port)
    gtk.main()

def main():

    args = sys.argv
    if len(args) < 2:
        print >> sys.stderr, "Usage: serve_mozilla.py module.class"
        sys.exit(-1)
    if '.' not in args[1]:
        print >> sys.stderr, "Usage: serve_mozilla.py module.class"
        sys.exit(-1)

    m, k = args[1].rsplit(".", 1)
    mod = __import__(m, fromlist=[k])
    klass = getattr(mod, k)

    run(klass)


