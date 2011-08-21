from exceptions import Exception

from rctk.task import Task


## "Synchronized attributes"
##
## Controls are represented both Client and Serverside. This means that their
## state needs to be synchronised on both, and possibly both ways.
## E.g. an update on a window title should actually change the title in the
## client, and resizing a window should update the width serverside.
##
## This synchronization is implemented using "Synchronized" attributes which
## need to be explicitly defined/configured on a control. Additionally, you
## can set the type of the attribute, this will help the XMLBuilder to properly
## parse datatypes in XML.
##
## In general, setting and getting attributes should be intercepted and possibly
## result in tasks being sent (which is up to the control inheriting from the
## AttributeHolder). It should be able to block updates (for example, on disabled
## or destroyed controls) and install a hook when an update has been done (so
## the Synchronized Attribute machinery doesn't need to bother about sending tasks
##
## Currently, which synchronization takes place is mostly up to the clientisde
## implementation: updates are always sent from server to client, but it may make
## sense to have specific fully serverside attributes that are not synchronized
## (but still properly configurable from xml)

class Attribute(object):
    """
        Attributes can be set on a AttributeHolder derived class. meta class
        magic will replace them using "interceptors" (AttributeInterceptor)
        that will catch/handle the setting/getting of the attribute.

        E.g.

        class MyControl(AttributeHolder):
            title = Attribute("Default title", Attribute.STRING)
            body = Attribute("", Attribute.STRING, filter=escape_html)
            lines = Attribute(20, Attribute.STRING)

        c = MyControl(title="Hello World")
        c.text = "<b>How are you!</b>"

        filtering is not actively used by the Synchronzed Attributes machinery,
        but can be used by the callback responsible for actually synchronizing.
        Filtering should be two-way. Implement a class with from/to?
    """

    STRING = 1
    NUMBER = 2
    BOOLEAN = 3

    def __init__(self, default="", type=STRING, filter=None):
        self.default = default
        self.type = type
        self.filter = filter

class AttributeInterceptor(object):
    """
        Attributes confgured on a class derived from AttributeHolder will be
        replaced by AttributeInterceptors to properly handle getting/setting
        values
    """
    def __init__(self, name):
        self.name = name

    def __get__(self, holder, type):
        return holder._sa_getattribute(self.name)

    def __set__(self, holder, value):
        holder._sa_setattribute(self.name, value)

class AttributeMetaclass(type):
    """
        Responsible from replacing Attribute declarations with an
        AttributeInterceptor, and storing the original Attribute declarations
    """
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
        This base class is to be used by classes that want to support 
        Synchronized Attributes. The meta class used will take care of
        injecting the attribute machinery.
    """
    __metaclass__ = AttributeMetaclass

    def __init__(self, **kw):
        self._sa_attributes = {}
        for k,v in self.attributes().iteritems():
            if k in kw and self.allow_update(k, kw[k]):
                self._sa_attributes[k] = kw[k]
                self.attribute_updated(k, kw[k])
            else:
                self._sa_attributes[k] = v.default

    def attributes(self):
        a = {}
        for k in dir(self):
            if k.startswith('_sa_'):
                v = getattr(self, k)
                if isinstance(v, Attribute):
                    a[k[4:]] = v # strip _sa_
        return a

    def synchronize(self, **attributes):
        """
            Perform an update on the attributes. This is assumed to be
            a "remote" update, which means we will not invoke a callback
            or do any allowed checks (also to avoid sending out updates
            again)
        """
        for k, v in self.attributes().iteritems():
            if k in attributes:
                self._sa_attributes[k] = attributes[k]

    def _sa_getattribute(self, name):
        return self._sa_attributes[name]

    def _sa_setattribute(self, name, value):
        if self.allow_update(name, value):
            self._sa_attributes[name] = value
        self.attribute_updated(name, value)

    def allow_update(self, name, value):
        """ Allow a base class to intercept the update of an attribute.
            Raising exceptions is allowed.
            When returning False, updating will simply not take place, but
            no exception will be thrown.
        """
        return True

    def attribute_updated(self, name, value):
        """ A hook for a baseclass to take action once an attribute
            has been updated.
        """
        pass

class ControlDestroyed(Exception):
    pass

class Control(AttributeHolder):
    """ any control in the UI, a window, button, text, etc """
    name = "base"

    containable = True # by default a control can be contained 
    _id = 0

    # control state
    INITIALIZING = 0
    CREATED = 1
    DESTROYED = 2
    state = INITIALIZING

    enabled = Attribute(True, Attribute.BOOLEAN)
    visible = Attribute(True, Attribute.BOOLEAN)
    width = Attribute(0, Attribute.NUMBER)
    height = Attribute(0, Attribute.NUMBER)
    align = Attribute(None)
    font = Attribute() # actually, a dict!
    foreground = Attribute()
    background = Attribute()
    border = Attribute() # ??
    margin = Attribute() # ??
    padding = Attribute() # ??
    css_class = Attribute()
    maxwidth = Attribute(0, Attribute.NUMBER)
    maxheight = Attribute(0, Attribute.NUMBER)
    debug = Attribute(False, Attribute.BOOLEAN)

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

    def allow_update(self, name, value):
        if self.state == Control.DESTROYED:
            raise ControlDestroyed("Cannot update %s: control is destroyed" % name)
        return True

    def attribute_updated(self, name, value):
        if self.state != Control.CREATED:
            return # don't generate tasks before creation

        ## XXX this can be done more efficiently. E.g. self.get_attribute(name)
        attribute = self.attributes()[name]
        filter = attribute.filter
        if filter:
            value = filter(value)
        self.tk.queue(Task("%s id %d attr %s update to '%s'" %
            (self.name, self.id, name, value),
                {
                    'control':self.name,
                    'id':self.id,
                    'action':'update',
                    'update':{name:value}
                }
            ))

    def sync(self, **data):
        """
            Attributes have changed on the clientside; update the attributes.
        """
        self.synchronize(**data)

    def data(self):
        """ return synchronisable data, apply filters if necessary """
        d = {}
        for k, v in self.attributes().iteritems():
            value = getattr(self, k)
            if v.filter:
                value = v.filter(value)
            d[k] = value
        return d

    def restore(self):
        self.create()

    def destroy(self):
        if self.parent:
            self.parent.remove(self)
        self.tk.queue(Task("Destroy %s id %d" % (self.name, self.id),
            { 'action':'destroy', 'id':self.id }))
        ## XXX does this need to be synced? We have an explicit destroy task
        self.state = Control.DESTROYED

    def __repr__(self):
        rid = getattr(self, 'id', -1)
        rstate = getattr(self, 'state', 'unknown')
        rname = getattr(self, 'name', 'unknown')

        return '<%s name="%s" id=%s state=%s>' % (self.__class__.__name__, rname, rid, rstate)

