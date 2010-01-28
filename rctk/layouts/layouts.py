class LayoutException(Exception):
    pass

class Layout(object):

    def config(self):
        return {'type':self.type}

    def add(self, control, **options):
        pass

class GridLayout(Layout):
    type = "grid"

    def __init__(self, rows=0, columns=1):
        self.rows = rows
        self.columns = columns

    def config(self):
        return {'type':self.type, 'rows':self.rows, 'columns':self.columns}

class BorderLayout(Layout):
    type = "border"

class FlexLayout(GridLayout):
    type = "flex-grid"

class FlowLayout(Layout):
    type = "flow"

class TabbedLayout(Layout):
    type = "tabbed"

class IvoLayout(Layout):
    """
        Experimental, new, flexible layoutmanager.

        Some issues:
        - needs proper cascading of layout(), starting at the toplevel/root
        - all cells are equally sized. This is not always desirable, i.e.
          when nesting
    """

    type = "ivo"

    def __init__(self, columns=1, expand_horizontal=False, expand_vertical=False):
        self.columns = columns
        self.expand_horizontal = expand_horizontal
        self.expand_vertical = expand_vertical

    def config(self):
        return {'type':self.type, 'columns':self.columns, 'expand_horizontal':self.expand_horizontal, 'expand_vertical':self.expand_vertical}


class IvoStaticGridLayout(IvoLayout):
    """ a layout with equal-sized cells """
    type = "ivo-static"

class IvoGridLayout(IvoLayout):
    """ a layout with scaling rows/columns """
    type = "ivo-grid"

