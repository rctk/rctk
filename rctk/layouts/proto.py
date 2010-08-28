import Tkinter

root = Tkinter.Tk()

top = Tkinter.Toplevel(height=200, width=200)
top.title("Test")
top.maxsize(800, 800)

f = Tkinter.Frame(top)
f.pack()

msg = Tkinter.Message(f, text="Hello World sdfdsf sdfsda " * 100)
msg.grid(row=0, column=0)
msg = Tkinter.Message(f, text="xxx xxx")
msg.grid(row=0, column=1)
msg = Tkinter.Message(f, text="xxx xxx")
msg.grid(row=1, column=0)
msg = Tkinter.Message(f, text="xxx xxx")
msg.grid(row=1, column=1)

root.mainloop()
