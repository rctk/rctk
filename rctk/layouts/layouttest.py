from rctkdemos.demos import serve_demo, standalone
from rctk.widgets import StaticText, Button, Window, Panel, Window
from rctk.layouts.newlayout import NewLayout

class W1(Window):
    def doit(self):
        self.setLayout(NewLayout(columns=3, padx=2, pady=3))

        self.append(StaticText(self.tk, "Win 1", background="red"), colspan=2)
        self.append(StaticText(self.tk, "Win 2", background="yellow"))
        self.append(StaticText(self.tk, "Win 3", background="green"), rowspan=2)
        self.append(StaticText(self.tk, "Win 4", background="orange"))
        self.append(StaticText(self.tk, "Win 5", background="blue"))
        self.append(StaticText(self.tk, "Win 6", background="pink"))
        self.append(StaticText(self.tk, "Win 7", background="grey"))
        self.append(StaticText(self.tk, "Win 8", background="brown"), rowspan=2, colspan=2)

        self.layout()

class W2(Window):
    def doit(self):
        self.setLayout(NewLayout(columns=3, static=True, rows=3, padx=1, pady=1))
        self.append(StaticText(self.tk, "NW", background="yellow"), sticky=NewLayout.NORTH|NewLayout.WEST)
        self.append(StaticText(self.tk, "N", background="orange"), sticky=NewLayout.NORTH)
        self.append(StaticText(self.tk, "NE", background="yellow"), sticky=NewLayout.NORTH|NewLayout.EAST)
        self.append(StaticText(self.tk, "W", background="orange"), sticky=NewLayout.WEST)
        self.append(StaticText(self.tk, "X\nCENTER\nX", background="red"), sticky=NewLayout.CENTER)
        self.append(StaticText(self.tk, "E", background="orange"), sticky=NewLayout.EAST)
        self.append(StaticText(self.tk, "SW", background="yellow"), sticky=NewLayout.SOUTH|NewLayout.WEST)
        self.append(StaticText(self.tk, "S", background="orange"), sticky=NewLayout.SOUTH)
        self.append(StaticText(self.tk, "SE", background="yellow"), sticky=NewLayout.SOUTH|NewLayout.EAST)
        self.layout()

class Demo(object):
    title = "New Layout"
    description = title

    def build(self, tk, parent):
        self.tk = tk
        self.parent = parent
        self.parent.setLayout(NewLayout(columns=2))

        self.parent.append(StaticText(tk, "Hello 1", background="red"))
        self.parent.append(StaticText(tk, "Hello 2", background="yellow"))
        self.parent.append(StaticText(tk, "Hello 3", background="green"))
        self.parent.append(StaticText(tk, "Hello 4", background="blue"))

        self.parent.layout()
        w1 = W1(tk, "Demo")
        w1.doit()

        w2 = W2(tk, "Stickyness")
        w2.doit()

Standalone = standalone(Demo)

if __name__ == '__main__':
    serve_demo(Demo)

