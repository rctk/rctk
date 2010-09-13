from rctk.widgets.control import Control

from rctk.layouts import GridLayout, LayoutException
from rctk.task import Task

import warnings

class Container(Control):
    """ A container can contain controls. It uses a layout manager
        to position them. The default layoutmanager is a gridlayout
        (vertical).

        A container has a default LayoutManager which can be changed
        as long as no controls have been added 
    """

    default_layout = GridLayout

    def __init__(self, tk, **properties):
        super(Container, self).__init__(tk, **properties)
        self._layout = self.default_layout()
        self._controls = []
        self._controls_args = {} ## for restoration

    ##
    ## Can't really be created but we don't want to hide the default
    ## control behaviour from derived classes

    def _add_append_task(self, control, args):
        self.tk.queue(Task("Append %d to %d"  % (control.id, self.id), args))

    def append(self, control, **args):
        """ adds a control to the window.
            args can provide layout instructions for the
            layoutmanager
        """
        if not control.containable:
            warnings.warn("Widget %s does not support appending to parent container" % control)
            return

        if self.id == control.id:
            warnings.warn("Refusing to add widget %s to itself" % control)
            return
        if control.parent:
            control.parent.remove(control)
        t = {'id':self.id, 'child':control.id, 'action':'append'}
        t.update(args)
        self._controls.append(control)
        control.parent = self
        control._append_args = t
        self._add_append_task(control, t)
        ## restoration
        self._controls_args[control] = t

        self._layout.append(control, **args)
    
    def remove(self, control):
        """ Removes a control from the window and moves it back into
            the factory.
        """
        if control in self._controls and self.id != control.id:
            t = {'id':self.id, 'child':control.id, 'action':'remove'}
            control.parent = None
            control._append_args = None
            self.tk.queue(Task('Remove %d from %d' % (control.id, self.id), t))
            del self._controls_args[control]
            self._controls.remove(control)
    
    def destroy(self):
        for c in self._controls:
            c.destroy()
        super(Container, self).destroy()
    
    def restore(self):
        self.create()
        self._add_layout_task(self._layout)
        ## Not root and not a toplevel
        #if self.id > 0 and self.parent is not None:
        #    print str(self._append_args)
        #    self.parent.append(self, **self._append_args)

        for c in self._controls:
            c.restore()
            self._add_append_task(c, self._controls_args.get(c, {})) 
    
    def _add_layout_task(self, layout):
        self.tk.queue(Task("Set layout %s on id %d" % (layout.type, self.id),
          {'id':self.id, 'action':'layout', 'type':self._layout.type, 'config':self._layout.config()}))
    
    def setLayout(self, layout):
        if self._controls_added():
            raise LayoutException("Can't change layout once controls have been added")
        self._layout = layout
        self._add_layout_task(layout)

    def layout(self):
        self.tk.queue(Task("Laying out id %d" % (self.id,),
          {'id':self.id, 'action':'relayout', 'config':self._layout.config()}))
    
    def _controls_added(self):
        return len(self._controls) > 0
    
