import Tkinter

root = Tkinter.Tk()

top = Tkinter.Toplevel(height=200, width=200)
top.title("Test")
top.maxsize(800, 800)

f = Tkinter.Frame(top)
f.pack()

msg1 = Tkinter.Message(f, text="Hello World sdfdsf sdfsda ")
msg1.grid(row=0, column=0)
msg = Tkinter.Message(f, text="xxx xxx")
msg.grid(row=0, column=1)
msg = Tkinter.Message(f, text="xxx xxx")
msg.grid(row=1, column=0)

def foo(*a, **b):
    msg1.config(text="Hello World sdfdsf sdfsda " * 100)
    
b = Tkinter.Button(f, text="Click me", command=foo)
b.grid(row=1, column=1)


root.mainloop()
