import simplejson

import os
import time

from rctk.widgets import Root
from rctk.event import ClickEvent, ChangeEvent, SubmitEvent
from rctk.task import Task

class Timer(object):
    def __init__(self, millis, handler, continuous=False):
        self.started = time.time()
        self.millis = millis
        self.handler = handler
        self.continuous = continuous # default is once
        self.times = 0 # how many times it has fired

    def __call__(self, event):
        self.times += 1
        self.handler(event)

    ## implement __del__ and / remove() ?

class TimerManager(object):
    """ manages timers """
    def __init__(self, tk):
        self.tk = tk
        self.timers = {}
        self.timercount = 0

    def set_timer(self, handler, millis):
        t = Timer(millis, handler, continuous=False)
        self.timers[self.timercount] = t
        self.tk.queue(
             Task("Timer installed, %d millisec, id %d" %
                  (millis, self.timercount),
                  {'action':'timer', 'id':self.timercount, 'milliseconds':millis}))
        self.timercount += 1
        return t

    def fire(self, id):
        if id in self.timers:
            t = self.timers[id]
            ## invoke the handler
            t(None)
            if not t.continuous:
                del self.timers[id]
            
class Toolkit(object):
    def __init__(self, app, *args, **kw):
        self.app = app
        self._queue = []
        self._controls = {}
        self._root = Root(self)
        self.args = args
        self.kw = kw
        self.timers = TimerManager(self)
        self.config = {}

    def add_control(self, control):
        self._controls[control.id] = control

    def create_control(self, control, **extra):
        ## assert control.id in self._controls ?
        taskdata = dict(control=control.name, id=control.id, action='create')
        taskdata.update(control.getproperties())
        taskdata.update(extra)

        self.queue(Task("Create " + repr(control), taskdata))

    def root(self):
        return self._root

    def queue(self, item):
        """ queue a new item """
        self._queue.append(item)

    def handle(self, method, **args):
        if method == "start":
            if len(self._controls) > 1:
                # app is already running, resume session by restoring UI
                ## restore is a recursive process, start with the root
                ## and toplevels
                self._root.restore()
                ## iterate over toplevels 
                #for id, c in self._controls.items():
                #    c.restore()
            else:
                self.app.run(self)
            return {"state":"started", "config":self.config}
        if method == "task" and 'queue' in args:
            queue = simplejson.loads(args['queue'])
            for task in queue:
                tasktype = task['method']
                id = int(task['id'])
                if tasktype == "event":
                    eventtype = task.get('type')
                    if eventtype == "timer":
                        self.timers.fire(id)
                    else:
                        control = self._controls[id]

                        if eventtype == "click":
                            control.click(ClickEvent(control))
                        elif eventtype == "change":
                            control.change(ChangeEvent(control))
                        elif eventtype == "submit":
                            control.submit(SubmitEvent(control))
                elif tasktype == "sync":
                    def un_unicode(d):
                        """ transform unicode keys to normal """
                        return dict((str(k), v) for (k,v) in d.iteritems())
                    control = self._controls[id]
                    control.sync(**un_unicode(task.get('data', {})))

        ## any other case, including "pop" which is not handled explicitly
        ## right now.
        if self._queue:
            tasks = [x.task() for x in self._queue]
            self._queue = []
            return tasks
        return []

    def set_timer(self, handler, millis):
        """ set a timer which fires once after "millis" milliseconds 

            returns a reference that can be used to delete the timer
            if neccesary
        """
        return self.timers.set_timer(handler, millis)

