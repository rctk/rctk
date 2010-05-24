# 
# see: http://code.google.com/p/rctk/wiki/XMLUIDefinition
#

import sys
import os
import StringIO

from xml.etree import ElementTree

from rctk.util import resolveclass

def NS(s): 
    """ add NS """
    return "{http://www.wxwidgets.org/wxxrc}" + s

def NONS(s):
    """ strip NS """
    return s[32:]

class SimpleXMLBuilder(object):
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

        ## only accept objects, for now
        for c in root.getchildren():
            if c.tag == NS("object"):
                self.handle_control(c, self.container)

    def handle_control(self, object, parent):
        klass = object.attrib['class']
        XMLControlRegistry[klass](self.tk, self.storage, parent, object)
        

class ControlImporter(object):
    def __init__(self, classid):
        self.control_class = resolveclass(classid)

    @property
    def name(self):
        return self.control_class.name

    def __call__(self, tk, storage, parent, object): 
        properties = {}
        flags = {}
        sub = []

        for c in object.getchildren():
            if c.tag == NS("object"):
                sub.append(c)
            elif c.tag == NS("flags"):
                for f in c.getchildren():
                    ## how to handle int vs string?
                    flags[NONS(f.tag)] = f.text.strip()
            else:
                properties[NONS(c.tag)] = c.text

        name = object.attrib['name']

        control = self.control_class(tk, **properties)
        setattr(storage, name, control)
        parent.append(control, **flags)

        ## add subobjects to it, if it has any
        for c in sub:
            klass = c.attrib['class']
            XMLControlRegistry[klass](tk, storage, control, c)

XMLControlRegistry = {}
XMLControlRegistry["Button"] = ControlImporter("rctk.widgets.button.Button")
XMLControlRegistry["StaticText"] = ControlImporter("rctk.widgets.statictext.StaticText")
XMLControlRegistry["CheckBox"] = ControlImporter("rctk.widgets.checkbox.CheckBox")
XMLControlRegistry["Text"] = ControlImporter("rctk.widgets.text.Text")
XMLControlRegistry["Password"] = ControlImporter("rctk.widgets.text.Password")
XMLControlRegistry["Date"] = ControlImporter("rctk.widgets.date.Date")
XMLControlRegistry["List"] = ControlImporter("rctk.widgets.list.List")
XMLControlRegistry["Dropdown"] = ControlImporter("rctk.widgets.dropdown.Dropdown")
XMLControlRegistry["Panel"] = ControlImporter("rctk.widgets.panel.Panel")
XMLControlRegistry["Window"] = ControlImporter("rctk.widgets.window.Window")
XMLControlRegistry["Grid"] = ControlImporter("rctk.widgets.grid.Grid")


if __name__ == '__main__':
    class dummy(object):
        tk = {}

    s = SimpleXMLBuilder(dummy())
    s.fromPath('/home/ivo/m3r/projects/rctk/tsjilp/tsjilp/tsjilp.xml')
