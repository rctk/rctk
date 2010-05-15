import sys
import os
import cgi

import http.server
import rctk

from rctk.toolkit import Toolkit

import json

basedir = os.path.dirname(rctk.__file__)

class PersistentRequestFactoryClass(object):
    def __init__(self, app):
        self.tk = Toolkit(app())

    def __call__(self, *args):
        return StandaloneHTTPServer(self.tk, *args)

class StandaloneHTTPServer(http.server.BaseHTTPRequestHandler):
    def __init__(self, tk, *args):
        self.tk = tk
        http.server.BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        if self.path.startswith("/static"):
            data = open(os.path.join(basedir, self.path[1:]), "rb").read()
            self.wfile.write(data)
        else: ## main.html or resources
            type, data = self.tk.serve(self.path[1:])
            self.send_response(200, "Ok")
            self.send_header("content-type", type)
            self.send_header("content-length", len(data))
            self.end_headers()

            self.wfile.write(data.encode('utf-8'))

    def do_POST(self):
        method = self.path[1:]
        length = self.headers.get('content-length', -1)
        q = self.rfile.read(int(length)).decode('utf-8')
        arguments = rctk.compat.parse_qs(q)
        ## parse_qs always (?) returns lists of values, we need individual 
        ## values
        for k in arguments:
            v = arguments[k]
            if isinstance(v, list):
                arguments[k] = v[0]
        res = self.tk.handle(method, **arguments)
        res = json.dumps(res)
        self.send_response(200, "Ok")
        self.send_header("content-type", "application/json")
        self.send_header("content-length", len(res))

        self.end_headers()


        self.wfile.write(res.encode('utf-8'))


import socket

class StandaloneServer(object):
    def __init__(self, klass):
        self.port = -1
        self.klass = klass

    def start(self):
        factory = PersistentRequestFactoryClass(self.klass)
        for i in range(31337, 31337 + 50):
            try:
                self.server = http.server.HTTPServer(('localhost', i), factory)
                self.port = i
                break
            except socket.error as e:
                if e.args[0] == 98: ## In use
                    continue
                raise
        self.server.serve_forever()          

def run(klass):
    server = StandaloneServer(klass)
    server.start()
    port = server.port
    if port == -1:
        print("Couldn't find an available port", file=sys.stderr)
        sys.exit(-1)

def main():

    args = sys.argv
    if len(args) < 2:
        print("Usage: serve_py3.py module.class", file=sys.stderr)
        sys.exit(-1)
    if '.' not in args[1]:
        print("Usage: serve_py3.py module.class", file=sys.stderr)
        sys.exit(-1)

    m, k = args[1].rsplit(".", 1)
    mod = __import__(m, fromlist=[k])
    klass = getattr(mod, k)

    print("A")
    run(klass)
    print("B")

if __name__ == '__main__':
    main()


