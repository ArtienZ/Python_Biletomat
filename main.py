from tkinter import *
import sqlite3
def Warning(msg,op=0):
    popup=Tk()
    App_gui.withdraw()
    def LeaveWar():
        if op==0:
            popup.destroy()
            App_gui.deiconify()
        else:
            popup.destroy()
            App_gui.destroy()
    popup.wm_title("POWIADOMIENIE ")
    label=Label(popup,text=msg,font="Helvetica 20 bold")
    label.pack(side="top",fill='x',pady=10)
    B1=Button(popup,text="Powrót",font="Helvetica 16",command=LeaveWar)
    B1.pack()
    popup.mainloop()
class MainWindow(Tk):

    def __init__(self,*args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        self.geometry("600x400")
        self.title("Automat biletowy MPK")
        container=Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.app_data = {"TotalCost": DoubleVar(),
                         "TotalCostZl": DoubleVar()
                         }
        # frame=TicketSelect(container,self)
        # frame.grid(row=0, column=0, sticky="nsew")
        # self.frames[TicketSelect]=frame
        # frame=Payment(container,self)
        # frame.grid(row=0, column=0, sticky="nsew")
        # self.frames[Payment]=frame
        self.frames = {}
        for Frame_Name in (TicketSelect,Payment):
            frame=Frame_Name(container,self)
            self.frames[Frame_Name]=frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(TicketSelect)
    def show_frame(self,cont):
        self.app_data["TotalCostZl"].set(f"{'%.2f' % (self.app_data['TotalCost'].get()/100.0)} zł")
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
            self.TicketsPrices.append(Row[0])
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
        self.TotalCost.configure(text=f"{str('%.2f' % (float(self.TotalCostZl.get())/100))} zl")

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
        self.DATA3 = self.controller.app_data["TotalCostZl"]
        self.CoinsIn=[]
        self.ToPay = Label(self, font="Helvetica 14 bold",textvariable=self.DATA3)
        self.InMachine = Label(self,font="Helvetica 14 bold", text="Wrzucono już: 0.0 zł")
        self.CoinMenu()
        Button(self, text="Zakończ", width=8, command=self.close_window2).grid(row=9, column=0)
        Button(self, text="Zapłać", width=8, command= self.Pay).grid(row=9, column=1)
        Button(self, text="Powrót", width=8, command=lambda: controller.show_frame(TicketSelect)).grid(row=9,column=5)
        self.ToPay.grid(row=2, column=4)
        self.InMachine.grid(row=3, column=4)
    def CoinMenu(self):

        self.c = self.conn.cursor()
        self.b= self.conn.cursor()
        self.c.execute("SELECT monety.nominal,monety.ilosc,monety.wartosc_w_gr FROM monety ORDER BY monety.wartosc_w_gr DESC")
        self.b.execute("SELECT banknoty.nominal,banknoty.ilosc,banknoty.wartosc_w_gr FROM banknoty ORDER BY banknoty.wartosc_w_gr DESC")
        self.RecordsC = self.c.fetchall()
        self.RecordsB=self.b.fetchall()
        i=0
        j=0
        for Row in self.RecordsC:
            self.MenuButtons.append(Button(self,bg='lightgray',command=lambda t=int(Row[2]):self.AddCoin(t),text=f"{Row[0]}",width=8,height=3).grid(row=j,column=i,sticky=W,pady=5,padx=5))
            i+=1
            if i%3==0:
                j+=1
                i=0
        i=0
        for Row in self.RecordsB:
            self.MenuButtons.append(Button(self,bg='lightgray',command=lambda t=int(Row[2]):self.AddCoin(t), text=f"{Row[0]}", width=8, height=3).grid(row=j, column=i, sticky=W, pady=5, padx=5))
            i+=1
        Label(self,font = "Helvetica 14",text="Ile monet chcesz wrzucić? ").grid(row=0,column=4)
        Entry(self, width=8,font = "Helvetica 14 bold",justify=CENTER, textvariable=self.HowManyCoins).grid(row=1,column=4)
    def AddCoin(self,type):
        for i in range(0,self.HowManyCoins.get()):
            self.AmountOfCoins.append(type)
        self.TotalCash.set(sum(self.AmountOfCoins))
        self.InMachine.configure(text=f"Wrzucono już: {'%.2f' % (sum(self.AmountOfCoins)/100)} zł")
    def Pay(self):
        if self.TotalCash.get()<self.DATA2.get():
            Warning("Wrzuciłeś za małą kwotę")
        else:
            AvalibleCash = [[0 for x in range(2)] for y in range(len(self.RecordsB)+len(self.RecordsC))]
            i=0
            for Row in self.RecordsB:
                AvalibleCash[i][0]=Row[2]
                AvalibleCash[i][1]=Row[1]
                i+=1
            for Row in self.RecordsC:
                AvalibleCash[i][0] = Row[2]
                AvalibleCash[i][1] = Row[1]
                i += 1
            print(AvalibleCash)
            for i in self.AmountOfCoins:
                for j in range(0,len(AvalibleCash)):
                    if i==AvalibleCash[j][0]:
                        AvalibleCash[j][1]+=1
                        break
            Change=self.TotalCash.get()-self.DATA2.get()
            ChangeTemp=Change
            i=0
            while Change>0:
                if AvalibleCash[i][0]<=Change:
                    temp=Change//AvalibleCash[i][0]
                    Change-=(AvalibleCash[i][0]*temp)
                    AvalibleCash[i][1]-=1
                    print(f"{AvalibleCash[i][0]} {temp} {Change}")
                else:
                    i+=1
            print(AvalibleCash)
            print(Change)
            self.p = self.conn.cursor()
            i=0
            for de,am in AvalibleCash:
                print(len(self.RecordsB))
                print(f"{de}    {am}")
                if i < len(self.RecordsB):
                    self.p.execute("""UPDATE banknoty SET ilosc=? WHERE wartosc_w_gr=?""",(am,de))
                else:
                    self.p.execute("""UPDATE monety SET ilosc=? WHERE wartosc_w_gr=?""",(am,de))
                i+=1
            self.conn.commit()
            print(f"Wrzucone monety {self.AmountOfCoins} kwota:{sum(self.AmountOfCoins)}")
            Warning(f"Dziękujemy za zakup \n Wydano: {'%.2f' % (ChangeTemp/100.)}",1)
    def WhenTotalChange(self):
        self.DATA2.update_idletasks()
    def close_window2(self):
        self.master.destroy()
        exit()

App_gui =MainWindow()
App_gui.mainloop()
