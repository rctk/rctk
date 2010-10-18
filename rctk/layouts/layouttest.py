from rctkdemos.demos import serve_demo, standalone
from rctk.widgets import StaticText, Button, Window, Panel
from rctk.layouts.newlayout import NewLayout

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

Standalone = standalone(Demo)

if __name__ == '__main__':
    serve_demo(Demo)

