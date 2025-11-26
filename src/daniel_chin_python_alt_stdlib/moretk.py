'''
tkinter gadgets and some util functions.  
`Msgbox`, `inputbox`, `screenCenter`, `StretchMessage`, `StretchPicture`, `ToughText`, `bilingualStringLen`.  
Run this file to see demo.  
'''
import tkinter as tk
import threading
from PIL import Image, ImageTk
from graphic_terminal import eastAsianStrLen

def screenCenter(root):
    root.update_idletasks()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    root.geometry("%dx%d+%d+%d" % (size + (x, y)))

class InputboxThread(threading.Thread):
    def __init__(self, msg, default):
        super(__class__,self).__init__()
        self.msg=msg
        self.default=default
        self.prelock = threading.Lock()
        self.lock=threading.Lock()
        self.prelock.acquire()
        self.start()
        self.prelock.acquire()
        self.lock.acquire()
    
    def run(self):
        with self.lock:
            self.prelock.release()
            
            default = str(self.default)
            confirmed = False
            root = tk.Tk()
            
            def confirm(event):
                nonlocal confirmed, root
                confirmed = True
                root.destroy()
            
            input = tk.StringVar(root)
            entry = tk.Entry(root,textvariable=input, font='Times 20')
            entry.bind('<Return>', confirm)
            input.set(default)
            entry.select_range(0, 'end')
            entry.icursor('end')
            
            label = tk.Label(root, text=self.msg, font='Courier 20') 
            
            label.grid()
            entry.grid(sticky='we')
            root.grid_columnconfigure(0, weight=1)
            screenCenter(root)
            entry.focus_force()
            root.mainloop()
            if confirmed:
                self.input = input.get()
            else:
                self.input = default

def inputbox(msg = '', default = ''):
    return InputboxThread(msg, default).input

class Msgbox(threading.Thread):
    def __init__(self, msg = '', title = '', blocking = True):
        super(__class__,self).__init__()
        self.msg=msg
        self.title = title
        self.condition = threading.Condition()
        self.has_ended = False
        self.do_end = False
        self.doEndLock = threading.Lock()
        self.blocking = blocking
        self.root = None
        self.start()
        if blocking:
            with self.condition:
                while not self.has_ended:
                    self.condition.wait()
            # ended. 
    
    def checkDoEnd(self):
        with self.doEndLock:
            if self.do_end:
                self.root.destroy()
                self.root.quit()
            else:
                self.root.after(10, self.checkDoEnd)
    
    def terminate(self):
        with self.doEndLock:
            self.do_end = True
        with self.condition:
            while not self.has_ended:
                self.condition.wait()
    
    def run(self):
        with self.condition:
            self.root = tk.Tk()
            root = self.root
            root.title(self.title)
            if not self.blocking:
                self.root.after(10, self.checkDoEnd)
            
            label = tk.Label(root, text=self.msg, font='Verdana 20') 
            label.pack(padx = 20, pady = 10)
            
            if self.blocking:
                button = tk.Button(root, text='OK', command=root.destroy)
                button.bind('<Return>', lambda event : (root.destroy()))
                button.pack(pady = (0, 10))
                button.focus_force()
            
            screenCenter(root)
            root.mainloop()
            del self.root
            self.has_ended = True
            self.condition.notify()

class StretchMessage(tk.Message):
    def __init__(self, master, **kw):
        if 'font' not in kw:
            kw['font'] = 'Times 20'
        super(__class__,self).__init__(master, **kw)
        self.bind('<Button-3>', self.displayText)
        master.handlers_to_convey.append(self.stretch)
    
    def stretch(self, event):
        self.config(width=event.width)
    
    def displayText(self,event):
        inputbox('You can copy now',self.cget('text'))
    
    def toughSetText(self, text):
        try:
            super(__class__,self).config(text = text)
        except:
            tempMessage = tk.Message(self.master)
            chunk = ''
            for char in text:
                try:
                    tempMessage.config(text = char)
                    chunk += char
                except:
                    chunk += '?'
            tempMessage.destroy()
            super(__class__,self).config(text = chunk)

class StretchPicture(tk.Frame):
    def __init__(self, master, image_path, keep_ratio = True, **kw):
        super(__class__,self).__init__(master, **kw)
        self.keep_ratio = keep_ratio
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.original = Image.open(image_path)
        self.photoImage = ImageTk.PhotoImage(self.original)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        self.canvas.create_image(0, 0, image=self.photoImage, anchor=tk.NW, tags="IMG")
        self.canvas.grid(row=0, sticky='wens')
        self.bind("<Configure>", self.resize)
        self.config(**kw)
    
    def pack(self):
        super(__class__,self).pack(fill=tk.BOTH, expand=1)
    
    def grid(self, **kw):
        super(__class__,self).grid(sticky='wens', **kw)
    
    def resize(self, event):
        if self.keep_ratio:
            ratio = self.original.size[0]/self.original.size[1]
            frame_ratio = event.width / event.height
            if ratio > frame_ratio:
                # Use width
                size = (event.width, int(event.width / ratio))
            else:
                # Use height
                size = (int(event.height * ratio), event.height)
        else:
            size = (event.width, event.height)
        resized = self.original.resize(size,Image.ANTIALIAS)
        self.photoImage = ImageTk.PhotoImage(resized)
        self.canvas.delete("IMG")
        self.canvas.create_image(int(event.width/2), 
            int(event.height/2), image=self.photoImage, anchor=tk.CENTER, tags="IMG")

class ToughText(tk.Text):
    def __init__(self, master, **kw):
        super(__class__,self).__init__(master, **kw)
    
    def insert(self, index, chars, *args):
        try:
            super(__class__,self).insert(index, chars, *args)
        except:
            if chars is None:
                return
            tempText = tk.Text(self.master)
            chunk = ''
            for char in chars:
                try:
                    tempText.insert(tk.END,char)
                    chunk += char
                except:
                    chunk += '?'
            tempText.destroy()
            super(__class__,self).insert(index, chunk, *args)

def bilingualStringLen(string, fontsize = 18):
    '''
    counts a chinese character as length of 2. 
    '''
    length = eastAsianStrLen(string, 2.2)
    length = int(length * fontsize / 18)
    return length

def makeStretcherParent(widget):
    widget.handlers_to_convey = []
    def stretchChildren(event):
        for handler in widget.handlers_to_convey:
            handler(event)
    widget.bind('<Configure>', stretchChildren)

if __name__=='__main__':
    Msgbox('asd')
