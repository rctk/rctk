from container import Container

class Root(Container):
    """ the root window. Unique, id 0 """
    name = "root"

    def __init__(self, tk):
        ## prevent id generation: don't call super
        self.tk = tk
        self.id = 0
        self.tk.add_control(self)
        self._controls_added = False
