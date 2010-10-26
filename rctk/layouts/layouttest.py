from rctkdemos.demos import serve_demo, standalone
from rctk.widgets import StaticText, Button, Window, Panel, Window
from rctk.layouts.newlayout import NewLayout

class W(Window):
    def doit(self):
        self.setLayout(NewLayout(columns=3))

        self.append(StaticText(self.tk, "Win 1"), colspan=2)
        self.append(StaticText(self.tk, "Win 2"))
        self.append(StaticText(self.tk, "Win 3"), rowspan=2)
        self.append(StaticText(self.tk, "Win 4"))
        self.append(StaticText(self.tk, "Win 5"))
        self.append(StaticText(self.tk, "Win 6"))
        self.append(StaticText(self.tk, "Win 7"))
        self.append(StaticText(self.tk, "Win 8"), rowspan=2, colspan=2)

        self.layout()

class Demo(object):
    title = "New Layout"
    description = title

    def build(self, tk, parent):
        self.tk = tk
        self.parent = parent
        self.parent.setLayout(NewLayout(columns=2))

        self.parent.append(StaticText(tk, "Hello 1"))
        self.parent.append(StaticText(tk, "Hello 2"))
        self.parent.append(StaticText(tk, "Hello 3"))
        self.parent.append(StaticText(tk, "Hello 4"))

        self.parent.layout()
        w = W(tk, "Demo")
        w.doit()


Standalone = standalone(Demo)

if __name__ == '__main__':
    serve_demo(Demo)

