from rctk.task import Task

class PropertyHolder(object):
    properties = {}

    def __init__(self, **properties):
        for (k, v) in self.properties.iteritems():
            setattr(self, k, properties.get(k, v))
        for k in properties:
            if k not in self.properties:
                raise KeyError("Unknown property %s" % k)

    @classmethod
    def extend(cls, **update):
        c = cls.properties.copy()
        c.update(update)
        return c

    def getproperties(self):
        return dict((k, getattr(self, k, self.properties[k])) for k in self.properties)

class Control(PropertyHolder):
    """ any control in the UI, a window, button, text, etc """
    name = "base"

    _id = 0

    properties = PropertyHolder.extend(width=0, height=0, foreground=None, background=None);

    def __init__(self, tk, **properties):
        super(Control, self).__init__(**properties)
        self.tk = tk
        self.id = self.newid()
        self._parent = None
        self._append_args = {}
        self.tk.add_control(self)
        self.create()

    def create(self):
        self.tk.create_control(self)

    @classmethod
    def newid(cls):
        ## first id will be 1, 0 is for Root window
        Control._id += 1
        return Control._id

    def sync(self, **data):
        """ 
            controls sometimes need synchronization, i.e. something has changed
            on the clientside
        """
        pass
        
    def restore(self):
        self.create()
    
    def __repr__(self):
        return '<%s name="%s" id=%d>' % (self.__class__.__name__, self.name, self.id)
    
class remote_attribute(object):
    """
        This descriptor class implements an easier way to
        sync specific attributes remotely.

        You need to pass it a name, the actual value will be
        stored on the context object under the same name prefixed
        with a '_'. This way you can safely bypass the descriptor
        if you don't want any tasks to be sent.
    """
    def __init__(self, name, default):
        """ setting a default does not set it remotely! """
        self.name = name
        self.default = default

    def __get__(self, control, type):
        return getattr(control, '_'+self.name, self.default)

    def __set__(self, control, value):
        setattr(control, '_'+self.name, value)
        control.tk.queue(Task("%s id %d attr %s update to '%s'" % 
                              (control.name, control.id, self.name, value),
            {
                'control':control.name,
                'id':control.id,
                'action':'update',
                'update':{self.name:value}
            }
        ))
