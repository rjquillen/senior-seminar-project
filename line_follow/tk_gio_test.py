from Tkinter import *
class Part3:

    def __init__(self, parent):

        GUIFrame =Frame(parent,width= 300, height=200)
        GUIFrame.pack(expand = False, anchor = CENTER)
        self.entry = Entry(text="enter your choice")
        self.entry.place(x=65, y = 10)
        self.test = StringVar()
        self.test.set('''Hi, I'm a Label :)''')
        self.Label1 = Label(parent, textvariable = self.test)
        self.Label1.place(x = 85, y = 100)
        self.Button2 = Button(parent, text='edit',command=self.LabelChange)
        self.Button2.place(x= 80, y = 60)
        self.Button3 = Button(parent, text='exit', command= parent.quit)
        self.Button3.place(x= 160, y = 60)


    def LabelChange(self):
        self.test.set(self.entry.get())

root = Tk()
MainFrame =Part3(root)
root.title('Input Test')
root.mainloop()
root.destroy()
