from tkinter import *
master = Tk()
def callback():
    print("click!")
 
b = Button(master, text="OK", command=callback)
#b.pack()
b.place(x=50,y=r100)
 
master.mainloop()
