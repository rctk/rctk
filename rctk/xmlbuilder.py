# 
# see: http://code.google.com/p/rctk/wiki/XMLUIDefinition
#

import sys
import os
import StringIO

from xml.etree import ElementTree

from rctk.util import resolveclass

import inspect

def getRequired(c):
    """ determine required arguments from a callable 'c'. Handle
        the case where c is actually a class or a generic callable
    
        This may not work with decorated functions or descriptors.
    """
    skipself = False
    f = c

    if not inspect.isfunction(c):
        if inspect.isclass(c):
            f = c.__init__
            skipself = True
        elif isinstance(c, (types.ObjectType, types.InstanceType)):
            f = c.__call__
            skipself = True
        # else? Just hope and try it works.    
    args, varargs, varkw, defaults = inspect.getargspec(f)
    if defaults:
        args = args[:-len(defaults)]

    if skipself and args[0] == "self":
        args.pop(0)
    return args 

def NS(s): 
    """ add NS """
    return "{http://www.wxwidgets.org/wxxrc}" + s

def NONS(s):
    """ strip NS """
    return s[32:]

class ParseError(Exception):
    pass

class SimpleXMLBuilder(object):
    """
        Import an entire xml file with all contained objects, adds
        them (as in .append()) to the supplied container.
        References to the individual controls will be stored in 'storage'
        under their respective names.
        container and storage can be the same object.
    """
    def __init__(self, container, storage=None):
        self.container = container
        self.storage = storage or container
        self.tk = container.tk

    def fromPath(self, path):
        ## some magic to allow paths relative to calling module
        if path.startswith('/'):
            fullpath = path
        else:
            frame = sys._getframe(1)
            base = os.path.dirname(frame.f_globals['__file__'])
            fullpath = os.path.join(base, path)
        xml = open(fullpath, "r").read()
        return self.fromString(xml)

    def fromString(self, xmlstr):
        tree = ElementTree.parse(StringIO.StringIO(xmlstr))
        root = tree.getroot()

        created = []
        ## only accept objects, for now
        for c in root.getchildren():
            if c.tag == NS("object"):
                klass = c.attrib['class']
                o = XMLControlRegistry[klass](self.tk, self.storage, 
                                          self.container, c, klass)
                created.append(o)
        return created

class XMLLoader(object):
    """
        Constructs controls entirely, not depending on a 
        container. It's up to the caller to append the 
        constructed control(s)

        Returns a list of controls. Also, individual controls can
        be loaded by supplying the name.
    """
    def __init__(self, tk):
        self.tk = tk
        
    def fromPath(self, path, names=None):
        ## some magic to allow paths relative to calling module
        ## XXX mostly duplicated from SimpleXMLBuilder
        if path.startswith('/'):
            fullpath = path
        else:
            frame = sys._getframe(1)
            base = os.path.dirname(frame.f_globals['__file__'])
            fullpath = os.path.join(base, path)
        xml = open(fullpath, "r").read()
        return self.fromString(xml, names)

    def fromString(self, xmlstr, names=None):
        """ load controls from an xml string. Optionally filter on names,
            only return controls that match """
        tree = ElementTree.parse(StringIO.StringIO(xmlstr))
        root = tree.getroot()

        created = {}
        ## only accept objects, for now
        for c in root.getchildren():
            if c.tag == NS("object"):
                klass = c.attrib['class']
                name = c.attrib['name']
                if names is None or name in names:
                    o = XMLControlRegistry[klass](self.tk, None, None, c, klass)
                    created[name] = o
        return created

class ControlImporter(object):
    def __init__(self, class_or_classid):
        import types

        if isinstance(class_or_classid, types.StringTypes):
            self.control_class = resolveclass(class_or_classid)
        else:
            self.control_class = class_or_classid

    @property
    def name(self):
        return self.control_class.name

    def __call__(self, tk, storage, parent, object, classname): 
        properties = {}
        flags = {}
        sub = []

        for c in object.getchildren():
            if c.tag == NS("object"):
                sub.append(c)
            elif c.tag == NS("flags"):
                for f in c.getchildren():
                    ## how to handle int vs string?
                    if NONS(f.tag) in ("row", "column", "colspan", "rowspan"):
                        flags[NONS(f.tag)] = int(f.text.strip())
                    else:
                        flags[NONS(f.tag)] = f.text.strip()
            elif c.tag == NS("items"):
                ## handle <items> to satisfy dropdown, list, etc
                items = []
                for ii in c.getchildren():
                    if ii.tag == NS("item"):
                        key, value = None, None
                        for i in ii.getchildren():
                            if i.tag == NS("key"):
                                key = i.text.strip()
                            if i.tag == NS("value"):
                                value = i.text
                        items.append((key, value))
                properties['items'] = items
            else:
                ## again typing issue
                properties[NONS(c.tag)] = c.text or ""

        name = object.attrib.get('name', None)

        missing = set(getRequired(self.control_class)).difference(properties.keys()) - set(["tk"])
        if missing:
            ## It would be nice to get the tags linenumber
            raise ParseError, "Missing required properties on <object class=\"%s\">: %s" % (classname, ", ".join(missing))

        try:
            control = self.control_class(tk, **properties)
        except TypeError, e:
            raise ParseError, "Failed to create <object class=\"%s\">: %s" % (classname, str(e))

        if name and storage:
            setattr(storage, name, control)
        if parent and control.containable:
            parent.append(control, **flags)

        ## add subobjects to it, if it has any
        for c in sub:
            klass = c.attrib['class']
            XMLControlRegistry[klass](tk, storage or control, control, c, klass)
        return control

class GridLayoutImporter(ControlImporter):
    """ A gridlayout isn't a new control, it's actually a pluggable
        configuration on the parent container. This means no actual
        new control should be created

        Also, the GridLayout is actually called "Grid" in python, which
        clashes with the Grid control
    """
    def __call__(self, tk, storage, parent, object, classname): 
        properties = {}
        sub = []

        for c in object.getchildren():
            if c.tag == NS("object"):
                sub.append(c)
            else:
                ## handle sticky, static, XXX
                if NONS(c.tag) in ("rows", "columns"):
                    properties[NONS(c.tag)] = int(c.text)
                else:
                    properties[NONS(c.tag)] = c.text


        layout = self.control_class(**properties)
        parent.setLayout(layout)

        ## handle subobjects. They're created on the parent,
        ## Not on the layout!
        for c in sub:
            klass = c.attrib['class']
            XMLControlRegistry[klass](tk, storage, parent, c, klass)
        return parent

class TabbedLayoutImporter(ControlImporter):
    """
    """
    def __call__(self, tk, storage, parent, object, classname): 
        properties = {}
        sub = []

        for c in object.getchildren():
            if c.tag == NS("object"):
                sub.append(c)
            else:
                pass ## tabbed layout has no configuration (yet)

        layout = self.control_class(**properties)
        parent.setLayout(layout)

        ## handle subobjects. They're created on the parent,
        ## Not on the layout!
        for c in sub:
            klass = c.attrib['class']
            XMLControlRegistry[klass](tk, storage, parent, c, klass)
        return parent

class GridImporter(ControlImporter):
    """ 
        Grids have nested column definitions
    """
    def __call__(self, tk, storage, parent, object, classname): 
        properties = {}
        flags = {}
        sub = []
        cols = []

        for c in object.getchildren():
            if c.tag == NS("object"):
                sub.append(c)
            elif c.tag == NS("flags"):
                for f in c.getchildren():
                    ## XXX duplication
                    ## how to handle int vs string?
                    if NONS(f.tag) in ("row", "column", "colspan", "rowspan"):
                        flags[NONS(f.tag)] = int(f.text.strip())
                    else:
                        flags[NONS(f.tag)] = f.text.strip()
            elif c.tag == NS("cols"):
                for col in c.getchildren():
                    colprops = {}
                    ## only handle col
                    if col.tag == NS("col"):
                        ## again, how to handle bool, int?
                        for prop in col.getchildren():
                            colprops[NONS(prop.tag)] = prop.text.strip()
                    cols.append(colprops)
            else:
                properties[NONS(c.tag)] = c.text

        from rctk.widgets.grid import Column

        columns = [Column(**p) for p in cols]

        name = object.get('name')

        control = self.control_class(tk, columns)
        if name:
            setattr(storage, name, control)
        parent.append(control, **flags)

        ## we're not handling the subs, grid's don't have any
        return parent

XMLControlRegistry = {}
XMLControlRegistry["Button"] = ControlImporter("rctk.widgets.button.Button")
XMLControlRegistry["Image"] = ControlImporter("rctk.widgets.image.Image")
XMLControlRegistry["StaticText"] = ControlImporter("rctk.widgets.statictext.StaticText")
XMLControlRegistry["StaticHTMLText"] = ControlImporter("rctk.widgets.statictext.StaticHTMLText")
XMLControlRegistry["CheckBox"] = ControlImporter("rctk.widgets.checkbox.CheckBox")
XMLControlRegistry["Text"] = ControlImporter("rctk.widgets.text.Text")
XMLControlRegistry["Password"] = ControlImporter("rctk.widgets.text.Password")
XMLControlRegistry["Date"] = ControlImporter("rctk.widgets.date.Date")
XMLControlRegistry["List"] = ControlImporter("rctk.widgets.list.List")
XMLControlRegistry["Dropdown"] = ControlImporter("rctk.widgets.dropdown.Dropdown")
XMLControlRegistry["Panel"] = ControlImporter("rctk.widgets.panel.Panel")
XMLControlRegistry["Window"] = ControlImporter("rctk.widgets.window.Window")
XMLControlRegistry["Grid"] = GridImporter("rctk.widgets.grid.Grid")

XMLControlRegistry["GridLayout"] = GridLayoutImporter("rctk.layouts.grid.GridLayout")
XMLControlRegistry["VBoxLayout"] = GridLayoutImporter("rctk.layouts.grid.VBox")
XMLControlRegistry["HBoxLayout"] = GridLayoutImporter("rctk.layouts.grid.HBox")

XMLControlRegistry["TabbedLayout"] = TabbedLayoutImporter("rctk.layouts.tabbed.TabbedLayout")

