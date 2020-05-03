from tkinter import *
import sqlite3

class MainWindow(Tk):
    frames = {}
    def __init__(self,*args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        self.geometry("800x600")
        self.title("Automat biletowy MPK")
        container=Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.app_data = {"TotalCost": DoubleVar()}
        # frame=TicketSelect(container,self)
        # frame.grid(row=0, column=0, sticky="nsew")
        # self.frames[TicketSelect]=frame
        # frame=Payment(container,self)
        # frame.grid(row=0, column=0, sticky="nsew")
        # self.frames[Payment]=frame
        for Frame_Name in (TicketSelect,Payment):
            frame=Frame_Name(container,self)
            self.frames[Frame_Name]=frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(TicketSelect)
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()
    def get_page(self, page_class):
        return self.frames[page_class]
class TicketSelect(Frame):
    def __init__(self, parent,controller):
        Frame.__init__(self,parent)
        self.parent=parent
        self.controller = controller
        self.TotalCostZl=self.controller.app_data["TotalCost"]
        self.ticketsarray = [0,0,0,0,0,0]
        self.labels = []
        self.AmountOfTicketsLabel = []
        self.TicketsPrices = []
        self.conn=sqlite3.connect('automat.db')
        self.TotalCost = Label(self, width=8, text=f"{self.TotalCostZl} zł")
        self.GetTicketsPrices()
        self.CreateLabels()
        self.cena=IntVar()
        self.cena.set(20)
        print(self.cena.get())
        Button(self, text="Zakoncz", width=20, command=self.close_window).grid(row=9, column=0, sticky=W)
        Button(self, text="Platnosc", width=20,command=lambda: controller.show_frame(Payment)).grid(row=9, column=5, sticky=E)
        self.TotalCost.grid(column=5, row=8)
    def WhenEChange(self,a,b,c):
        for i in range(0,len(self.ticketsarray)):
            try:
                temp=self.ticketsarray[i].get()
            except:
                self.ticketsarray[i].set(0)
            if temp<0:
                self.ticketsarray[i].set(0)
            self.AmountOfTicketsLabel[i].update_idletasks()
        self.AmountOfTicketsLabel[i].update_idletasks()
        self.CalTotalCost()
    def CreateLabels(self):
        del self.labels[:]
        del self.AmountOfTicketsLabel[:]
        del self.ticketsarray[:]
        print(len(self.ticketsarray))
        self.c = self.conn.cursor()
        self.c.execute('SELECT nazwa,cena FROM bilety ORDER BY Id_biletu')
        Records = self.c.fetchall()
        self.i = 0
        for Row in Records:
            self.ticketsarray.append(IntVar())
            self.ticketsarray[self.i].set(0)
            self.labels.append(Label(self, text=f"{Row[0]} {Row[1]/100:.2f} zł"))
            self.labels[self.i].grid(column=0, row=self.i + 2, pady=15)
            self.AmountOfTicketsLabel.append(Entry(self,justify=CENTER,command=self.CalTotalCost(),text="0", width=5, textvariable=self.ticketsarray[self.i]))
            self.AmountOfTicketsLabel[self.i].grid(column=4, row=self.i + 2, pady=15)
            Button(self, text="+", width=4, command=lambda i=self.i: self.clickplus(i)).grid(row=self.i + 2, column=3, sticky=W)
            Button(self, text="-", width=4, command=lambda i=self.i: self.clickminus(i)).grid(row=self.i + 2, column=5, sticky=W)
            self.ticketsarray[self.i].trace("w",self.WhenEChange)
            self.i = self.i + 1
    def GetTicketsPrices(self):
        del self.TicketsPrices[:]
        p = self.conn.cursor()
        p.execute('SELECT cena FROM bilety ORDER BY Id_biletu')
        Records = p.fetchall()
        for Row in Records:
            self.TicketsPrices.append(Row[0]/100)
    def clickplus(self,number):
        temp=self.ticketsarray[number].get()
        self.ticketsarray[number].set(temp+1)
        #self.AmountOfTicketsLabel[number].delete(0, END)
        #self.AmountOfTicketsLabel[number].insert(0, self.ticketsarray[number].get())
        self.CalTotalCost()

    def clickminus(self,number):
        temp = self.ticketsarray[number].get()
        if temp > 0:
            self.ticketsarray[number].set(temp-1)
            #self.AmountOfTicketsLabel[number].delete(0,END)
            #self.AmountOfTicketsLabel[number].insert(0,self.ticketsarray[number].get())
        self.CalTotalCost()
    def CalTotalCost(self):
        temp=0.0
        for j in range(len(self.ticketsarray)):
            temp += self.ticketsarray[j].get() * self.TicketsPrices[j]
        self.TotalCostZl.set(temp)
        self.TotalCost.configure(text=f"{str('%.2f' % self.TotalCostZl.get())} zl")

    def close_window(self):
        self.master.destroy()
        exit()
class Payment(Frame):
    def __init__(self, parent,controller):
        Frame.__init__(self, parent)
        self.controller=controller
        self.conn = sqlite3.connect('automat.db')
        self.AmountOfCoins=[]
        self.MenuButtons=[]
        self.HowManyCoins = IntVar()
        self.HowManyCoins.set(1)
        self.TotalCash=DoubleVar()
        self.Page1=self.controller.get_page(TicketSelect)
        self.DATA2 = self.controller.app_data["TotalCost"]
        self.CoinsIn=Label(self, width=8, text=" ")
        self.CoinMenu()
        Button(self, text="Zakończ", width=8, command=self.close_window2).grid(row=9, column=0)
        Button(self, text="Zapłać", width=8, command= self.Pay).grid(row=9, column=1)
        Button(self, text="Powrót", width=8, command=lambda: controller.show_frame(TicketSelect)).grid(row=9,column=5)
        self.CoinsIn.grid(row=8,column=5)
    def CoinMenu(self):
        self.c = self.conn.cursor()
        self.b=self.conn.cursor()
        self.c.execute("SELECT monety.nominal,monety.ilosc,monety.wartosc_w_gr FROM monety ORDER BY ID_monety")
        self.b.execute("SELECT banknoty.nominal,banknoty.ilosc,banknoty.wartosc_w_gr FROM banknoty ORDER BY Id_banknotu")
        RecordsC = self.c.fetchall()
        RecordsB=self.b.fetchall()
        i=0
        j=0
        for Row in RecordsC:
            self.MenuButtons.append(Button(self,bg='lightgray',command=lambda t=int(Row[2]):self.AddCoin(t),text=f"{Row[0]}",width=8,height=3).grid(row=j,column=i,sticky=W,pady=5,padx=5))
            i+=1
            if i%3==0:
                j+=1
                i=0
        i=0
        for Row in RecordsB:
            self.MenuButtons.append(Button(self,bg='lightgray',command=lambda t=int(Row[2]):self.AddCoin(t), text=f"{Row[0]}", width=8, height=3).grid(row=j, column=i, sticky=W, pady=5, padx=5))
            i+=1
        Label(self,font = "Helvetica 14",text="Ile monet chcesz wrzucić? ").grid(row=0,column=4)
        Entry(self, width=8,font = "Helvetica 14 bold",justify=CENTER, textvariable=self.HowManyCoins).grid(row=1,column=4)
        self.HowManyCoins.trace("w",lambda _:self.WhenTotalChange(self.HowManyCoins))
        Label(self,font = "Helvetica 14 bold",textvariable=self.DATA2).grid(row=2,column=4)
    def AddCoin(self,type):
        self.CoinsIn.configure(text=f"{type/100} zł")
        self.AmountOfCoins.append(type/100)
        self.TotalCash.set(sum(self.AmountOfCoins))
    def Pay(self):
        print(f"Wrzucone monety {self.AmountOfCoins} kwota:{sum(self.AmountOfCoins)}")
    def WhenTotalChange(self):
        self.HowManyCoins.update_idletasks()
    def close_window2(self):
        self.master.destroy()
        exit()


App_gui =MainWindow()
App_gui.mainloop()
