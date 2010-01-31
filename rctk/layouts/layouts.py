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

class TabbedLayout(Layout):
    type = "tabbed"

class Power(Layout):
    """
        New layoutmanager. Replaces the previous JLayout based 
        implementations. This is the mega-manager that can do
        everything, it's easier to use one of the specialized
        subclasses
    """

    type = "power"

    def __init__(self, rows=0, columns=1, expand_horizontal=False, expand_vertical=False,
                       flex=False):
        self.columns = columns
        self.rows = rows
        self.flex = flex
        self.expand_horizontal = expand_horizontal
        self.expand_vertical = expand_vertical

    def config(self):
        return {'type':self.type, 'columns':self.columns, 'rows':self.rows, 'expand_horizontal':self.expand_horizontal, 'expand_vertical':self.expand_vertical, 'flex':self.flex }

class Grid(Power):
    """
        Lays out controls in a grid. Dimensions can be explicitly defined,
        or derived from the specified number of rows, columns and the number
        of controls. The cells are sized dynamically (row/column-wise)

        Supports explicit positioning using row/column coordinates and
        row/colspan.
    """
    def __init__(self, rows=0, columns=1, expand_horizontal=False, 
                 expand_vertical=False):
        super(GridLayout, self).__init__(rows, columns, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=True)
# the name GridLayout is deprecated. Let's not append Layout everywhere in a
# module named "layout"
GridLayout = Grid 

class StaticGridLayout(Power):
    """
        Lays out controls in a grid. Dimensions can be explicitly defined,
        or derived from the specified number of rows, columns and the number
        of controls. The cells are fixed size: the size of the largest control.

        Supports explicit positioning using row/column coordinates and
        row/colspan.
    """
    def __init__(self, rows=0, columns=1, expand_horizontal=False, 
                 expand_vertical=False):
        super(StaticGridLayout, self).__init__(rows, columns, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=False)
class HBox(Power):
    """
        Lays out controls in a horizontal box (1 row). The width of
        individual cells are flexible

        Colspan and absolute positioning are supported
    """
    def __init__(self, expand_horizontal=False, expand_vertical=False):
        super(HBox, self).__init__(rows=1, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=False)

class StaticHBox(Power):
    """
        Lays out controls in a horizontal box (1 row). The width of
        individual cells are fixed: the width of the largest control.

        Colspan and absolute positioning are supported
    """
    def __init__(self, expand_horizontal=False, expand_vertical=False):
        super(GridLayout, self).__init__(columns=1, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=True)

class VBox(Power):
    """
        Lays out controls in a vertical box (1 column). The height of
        individual cells are flexible

        Rowspan and absolute positioning are supported
    """
    def __init__(self, expand_horizontal=False, expand_vertical=False):
        super(VBox, self).__init__(columns=1, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=False)

class StaticVBox(Power):
    """
        Lays out controls in a vertical box (1 column). The height of
        individual cells are flexible: the height of the largest control

        Rowspan and absolute positioning are supported
    """
    def __init__(self, expand_horizontal=False, expand_vertical=False):
        super(StaticVBox, self).__init__(rows=1, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=True)
