from tkinter import *
import sqlite3

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Automat biletowy MPK")
        master.geometry('800x400')
        self.ticketsarray = [0,0,0,0,0,0]
        self.TotalCostZl = 0
        self.labels = []
        self.AmountOfTicketsLabel = []
        self.TicketsPrices = []
        self.conn=sqlite3.connect('automat.db')
        self.TotalCost = Label(master, width=8, text=str(self.TotalCostZl) + 'zl')
        self.GetTicketsPrices()
        self.CreateLabels()
        self.cena=IntVar()
        self.cena.set(20)
        print(self.cena.get())
        Button(master, text="Zakoncz", width=20, command=self.close_window).grid(row=9, column=0, sticky=W)
        Button(master, text="Platnosc", width=20, command=self.close_window).grid(row=9, column=5, sticky=E)
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
            self.labels.append(Label(self.master, text=f"{Row[0]} {Row[1]/100:.2f} zł"))
            self.labels[self.i].grid(column=0, row=self.i + 2, pady=15)
            self.AmountOfTicketsLabel.append(Entry(self.master,command=self.CalTotalCost(),text="0", width=5, textvariable=self.ticketsarray[self.i]))
            self.AmountOfTicketsLabel[self.i].grid(column=4, row=self.i + 2, pady=15)
            Button(self.master, text="+", width=4, command=lambda i=self.i: self.clickplus(i)).grid(row=self.i + 2, column=3, sticky=W)
            Button(self.master, text="-", width=4, command=lambda i=self.i: self.clickminus(i)).grid(row=self.i + 2, column=5, sticky=W)
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
        self.TotalCostZl = 0.0
        for j in range(len(self.ticketsarray)):
            self.TotalCostZl += self.ticketsarray[j].get() * self.TicketsPrices[j]
        self.TotalCost.configure(text=str("%.2f" % self.TotalCostZl) + 'zl')
    def close_window(self):
        self.master.destroy()
        exit()
root = Tk()
App_gui = MainWindow(root)
root.mainloop()
