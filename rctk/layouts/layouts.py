class LayoutException(Exception):
    pass

class Layout(object):

    def config(self):
        return {'type':self.type}

    def add(self, control, **options):
        pass

class TabbedLayout(Layout):
    type = "tabbed"

class PowerLayout(Layout):
    """
        Experimental, new, flexible layoutmanager.

        Some issues:
        - needs proper cascading of layout(), starting at the toplevel/root
        - all cells are equally sized. This is not always desirable, i.e.
          when nesting
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

class GridLayout(PowerLayout):
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
class StaticGridLayout(PowerLayout):
    """
        Lays out controls in a grid. Dimensions can be explicitly defined,
        or derived from the specified number of rows, columns and the number
        of controls. The cells are fixed size: the size of the largest control.

        Supports explicit positioning using row/column coordinates and
        row/colspan.
    """
    def __init__(self, rows=0, columns=1, expand_horizontal=False, 
                 expand_vertical=False):
        super(GridLayout, self).__init__(rows, columns, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=False)
class HBox(PowerLayout):
    """
        Lays out controls in a horizontal box (1 row). The width of
        individual cells are flexible

        Colspan and absolute positioning are supported
    """
    def __init__(self, expand_horizontal=False, expand_vertical=False):
        super(GridLayout, self).__init__(rows=1, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=False)

class StaticHBox(PowerLayout):
    """
        Lays out controls in a horizontal box (1 row). The width of
        individual cells are fixed: the width of the largest control.

        Colspan and absolute positioning are supported
    """
    def __init__(self, expand_horizontal=False, expand_vertical=False):
        super(GridLayout, self).__init__(columns=1, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=True)

class VBox(PowerLayout):
    """
        Lays out controls in a vertical box (1 column). The height of
        individual cells are flexible

        Rowspan and absolute positioning are supported
    """
    def __init__(self, expand_horizontal=False, expand_vertical=False):
        super(GridLayout, self).__init__(columns=1, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=False)

class StaticVBox(PowerLayout):
    """
        Lays out controls in a vertical box (1 column). The height of
        individual cells are flexible: the height of the largest control

        Rowspan and absolute positioning are supported
    """
    def __init__(self, expand_horizontal=False, expand_vertical=False):
        super(GridLayout, self).__init__(rows=1, expand_horizontal=expand_horizontal, 
                                         expand_vertical=expand_vertical, flex=True)
