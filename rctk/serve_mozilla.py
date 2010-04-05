import sys

try:
    import gtk
    import gtkmozembed
except ImportError, e:
    print >> sys.stderr, "You need pygtk and gtkmozembed installed for this appserver to work"
    sys.exit(-1)

import BaseHTTPServer
import rctk
import os.path
import cgi

from rctk.toolkit import Toolkit
from rctkdemos.all import Demo

import gobject
import simplejson

basedir = os.path.dirname(rctk.__file__)

tk = Toolkit(Demo())

class StandaloneHTTPServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        print "GET", self.path
        if self.path == '/':
            main = os.path.join(basedir, 'main.html')
            print >> self.wfile,  open(main, "r").read()
        elif self.path.startswith("/static"):
            data = open(os.path.join(basedir, self.path[1:]), "r").read()
            print >> self.wfile, data

    def do_POST(self):
        print "POST", self.path
        method = self.path[1:]
        length = self.headers.get('content-length', -1)
        q = self.rfile.read(int(length))
        print "Q", q
        arguments = cgi.parse_qs(q)
        for k in arguments:
            v = arguments[k]
            if isinstance(v, list):
                arguments[k] = v[0]
        res = tk.handle(method, **arguments)
        res = simplejson.dumps(res)
        self.send_response(200, "Ok")
        self.send_header("content-type", "application/json")
        self.send_header("content-length", len(res))

        self.end_headers()


        print >> self.wfile, res
        # print "RES", res



## http://majorsilence.com/pygtk_embedded_web_browsers
class StandaloneRCTK(): 
    def __init__(self):
        self.moz = gtkmozembed.MozEmbed()
                
        self.server = BaseHTTPServer.HTTPServer(('', 31337), StandaloneHTTPServer)
        gobject.io_add_watch(self.server.socket, gobject.IO_IN, self.handle_request)
        win = gtk.Window()
        win.set_size_request(1200, 800)
        # win.set_size_request(12, 8)
        win.add(self.moz)
        win.show_all()
        self.moz.load_url('http://localhost:31337')

    def handle_request(self, *a):
        self.server.handle_request()
        return True

def main():
    s = StandaloneRCTK()
    gtk.main()
