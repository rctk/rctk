import web
import simplejson

import os

from rctk.widgets import Root
from rctk.event import ClickEvent, ChangeEvent

##
## headers: web.header(a,b) ?
#

class Toolkit(object):
    def __init__(self, app, *args, **kw):
        self.app = app
        self._queue = []
        self._controls = {}
        self._root = Root(self)
        self.args = args
        self.kw = kw

    def add_control(self, id, control):
        self._controls[id] = control

    def root(self):
        return self._root

    def queue(self, item):
        """ queue a new item """
        self._queue.append(item)

    def handle(self, method, **args):
        if method == "start":
            self.app.run(self)
            return {"state":"started"}
        elif method == "event":
            ## data gets submitted as form, not as json
            id = int(args['id'])
            control = self._controls[id]

            if args.get('type') == "click":
                control.click(ClickEvent(control))
            elif args.get('type') == "change":
                control.change(ChangeEvent(control))
        elif method == "sync":
            ## a control needs synchronization
            id = int(args['id'])
            control = self._controls[id]
            control.sync(**args)

        ## any other case, including "pop" which is not handled explicitly
        ## right now.
        if self._queue:
            tasks = [x.task() for x in self._queue]
            self._queue = []
            return tasks
        return []


class WebPyTK(Toolkit):
    def GET(self, data):
        data = data.strip()
        if not data:
            web.header("content-type", "text/html")
            return open(os.path.join(os.path.dirname(__file__), "main.html"), "r").read()

    def POST(self, data):
        web.header("content-type", "application/json")
        method = data.strip()
        arguments = web.input()

        result = super(WebPyTK, self).handle(method, **arguments)
        return simplejson.dumps(result)


