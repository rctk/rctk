from control import Control

from rctk.layouts import GridLayout, LayoutException
from rctk.task import Task

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
        self._controls_added = False

    ##
    ## Can't really be created but we don't want to hide the default
    ## control behaviour from derived classes

    def append(self, control, **args):
        """ adds a control to the window.
            args can provide layout instructions for the
            layoutmanager
        """
        self._controls_added = True
        if self.id != control.id:
            t = {'id':self.id, 'child':control.id, 'action':'append'}
            t.update(args)
            self.tk.queue(Task("Append %d to %d"  % (control.id, self.id), t));

    def setLayout(self, layout):
        if self._controls_added:
            raise LayoutException("Can't change layout once controls have been added")

        self._layout = layout

        self.tk.queue(Task("Set layout %s on id %d" % (layout.type, self.id),
          {'id':self.id, 'action':'layout', 'type':self._layout.type, 'config':self._layout.config()}))

    def layout(self):
        self.tk.queue(Task("Laying out id %d" % (self.id,),
          {'id':self.id, 'action':'relayout'}))

