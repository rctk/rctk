##
## TODO:
##
## - use layout to send the actual append() task. this way the 
##   LM can properly check the passed constraints and do local
##   calculations of necessary
## - support more constraints (top/left/.. alignment, expanding)

class LayoutException(Exception):
    pass

class Layout(object):

    def config(self):
        return {'type':self.type}

    def append(self, control, **kw):
        pass

