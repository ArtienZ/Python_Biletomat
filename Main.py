import tkinter as tk
from tkinter import font as tkfont
class MyApp(tk.Frame):
    def _init_(self):
        tk.Tk.__init__(self)
        self._frame=None
        self.title_font=tkfont.Font(family='Roboto',size=18,weight='bold')
        self.switch_frame(StartPage)
    def switch_frame(self,frame_class):
        new_frame=frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame=new_frame
        self.frame.pack()

class StartPage(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="Start Page").pack(sike='top',fill='x',pady=5)
        tk.Button(self,text='Go to page one',command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self,text='Go to page two',command=lambda: master.switch_frame(PageTwo)).pack()

class PageOne(tk.Frame):
    def __init__(self,master):
        tk.Frame._init_(self,master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self,text='Page one').pack(side='top',fill='x',pady=5)
        tk.Button(self, text='Go back to start page', command=lambda: master.switch_frame(StartPage)).pack()
class PageTwo(tk.Frame):
    def __init__(self,master):
        tk.Frame._init_(self,master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self,text='Page Two').pack(side='top',fill='x',pady=5)
        tk.Button(self, text='Go back to start page', command=lambda: master.switch_frame(StartPage)).pack()
if __name__=="__main__":
    app=MyApp()
    app.mainloop()