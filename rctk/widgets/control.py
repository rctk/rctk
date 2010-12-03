from exceptions import Exception

from rctk.task import Task


class ControlDestroyed(Exception):
    pass


##
## TODO: Special storage for attributes (so you don't need to define
## your own _foo)
## type definitions / general enumeration of settable properties (for xml)
## don't 'sync' properties if control is not created, when creating initialize

## "Synchronized attributes"

class Attribute(object):
    """
        The base attribute class for defining/configuring
        attributes 
    """

    STRING = 1
    NUMBER = 2

    def __init__(self, default, type=STRING, filter=None):
        self.default = default
        self.type = type
        self.filter = filter

class AttributeInterceptor(object):
    """ Intercept get/set on syncedattributes and forward them to
        the AttributeHolder """
    def __init__(self, name):
        self.name = name

    def __get__(self, holder, type):
        return holder._sa_getattribute(self.name)

    def __set__(self, holder, value):
        holder._sa_setattribute(self.name, value)

class AttributeMetaclass(type):
    def __new__(meta, classname, bases, classDict):
        newdict = {}
        for k, v in classDict.iteritems():
            if isinstance(v, Attribute):
                newdict['_sa_'+k] = v
                newdict[k] = AttributeInterceptor(k)
            else:
                newdict[k] = v

        return type.__new__(meta, classname, bases, newdict)

class AttributeHolder(object):
    """
        baseclass for objects (controls) that support "remote" attributes,
        i.e. attributes that are synchronized locally/remotely, possibly
        both ways
    """
    __metaclass__ = AttributeMetaclass

    def __init__(self):
        self._sa_attributes = {}
        for k,v in self.attributes().iteritems():
            self._sa_attributes[k] = v.default
        self.state = 0 ## tmp hack

    def attributes(self):
        a = {}
        for k in dir(self):
            if k.startswith('_sa_'):
                v = getattr(self, k)
                if isinstance(v, Attribute):
                    a[k[4:]] = v # strip _sa_
        return a

    def _sa_getattribute(self, name):
        return self._sa_attributes[name]

    def _sa_setattribute(self, name, value):
        ## odd dependency...
        if self.state == Control.DESTROYED:
            raise ControlDestroyed
        self._sa_attributes[name] = value
        ## invoke sync magic, if created...

    def sync_attribute(self, name):
        if self.created:
            self.tk.queue(Task("%s id %d attr %s update to '%s'" %
                                  (self.name, self.id, name, value),
                {
                    'control':self.name,
                    'id':self.id,
                    'action':'update',
                    'update':{self.name:self.filter(control, value)}
                }
            ))


class remote_attribute(object):
    """
        XXX deprecated, to be replaced/removed
        This descriptor class implements an easier way to
        sync specific attributes remotely.

        You need to pass it a name, the actual value will be
        stored on the context object under the same name prefixed
        with a '_'. This way you can safely bypass the descriptor
        if you don't want any tasks to be sent.
    """
    def __init__(self, name, default, filter=lambda control, x: x):
        """ setting a default does not set it remotely! """
        self.name = name
        self.default = default
        self.filter = filter

    def __get__(self, control, type):
        return getattr(control, '_'+self.name, self.default)

    def __set__(self, control, value):
        if control.state == Control.DESTROYED:
            raise ControlDestroyed
        else:
            setattr(control, '_'+self.name, value)
            control.tk.queue(Task("%s id %d attr %s update to '%s'" %
                                  (control.name, control.id, self.name, value),
                {
                    'control':control.name,
                    'id':control.id,
                    'action':'update',
                    'update':{self.name:self.filter(control, value)}
                }
            ))


class PropertyHolder(object):
    #   XXX deprecated, to be replaced/removed
    properties = {}

    def __init__(self, **properties):
        for (k, v) in self.properties.items():
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

    containable = True # by default a control can be contained 
    _id = 0

    # control state
    ENABLED = 0
    DISABLED = 1
    DESTROYED = 2

    state = remote_attribute("state", ENABLED)
    visible = remote_attribute("visible", True)
    properties = PropertyHolder.extend(
        width=0, height=0, align=None,
        font=None, foreground=None, background=None,
        border=None, margin=None, padding=None,
        css_class=None,
        maxwidth=0,
        maxheight=0,
        debug=False
    )

    def __init__(self, tk, **properties):
        super(Control, self).__init__(**properties)
        self.tk = tk
        self.id = self.newid()
        self.parent = None
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

    def destroy(self):
        if self.parent:
            self.parent.remove(self)
        self.tk.queue(Task("Destroy %s id %d" % (self.name, self.id),
            { 'action':'destroy', 'id':self.id }))
        self._state = Control.DESTROYED

    def __repr__(self):
        ## some state may be unitialized when crashing
        rid = getattr(self, 'id', -1)
        rstate = getattr(self, 'state', 'unknown')
        rname = getattr(self, 'name', 'unknown')

        return '<%s name="%s" id=%s state=%s>' % (self.__class__.__name__, rname, rid, rstate)




