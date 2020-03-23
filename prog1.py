import sqlite3
from tkinter import *
conn = sqlite3.connect('automat.db')
ticketsarray=[0,0,0,0,0,0]
TotalCostZl=0
labels=[]
AmountOfTicketsLabel=[]
TicketsPrices=[]
window = Tk()
window.option_add( "*font", "lucida 16 bold" )
window.geometry('800x480')
window.title('Automat biletowy MPK')
window.configure(background='white')
def GetTicketsPrices():
    del TicketsPrices[:]
    p=conn.cursor()
    p.execute('SELECT cena FROM bilety ORDER BY Id_biletu')
    Records=p.fetchall()
    for Row in Records:
        TicketsPrices.append(Row[0])
def CreateLabels():
    del labels[:]
    del AmountOfTicketsLabel[:]
    c = conn.cursor()
    c.execute('SELECT nazwa,cena FROM bilety ORDER BY Id_biletu')
    Records=c.fetchall()
    i=0
    for Row in Records:
        labels.append(Label(window,text=f"{Row[1]:02} zł"))
        labels[i].grid(column=0,row=i+2, pady=15)
        AmountOfTicketsLabel.append(Label(window,width=5,text=ticketsarray[i]))
        AmountOfTicketsLabel[i].grid(column=4,row=i+2,pady=15)
        print("i= " +str(i))
        Button(window, text="+", width=4, command=lambda i=i: clickplus(i)).grid(row=i+2, column=3,sticky=W)
        Button(window, text="-", width=4, command=lambda i=i: clickminus(i)).grid(row=i+2, column=5,sticky=W)
        print(str(AmountOfTicketsLabel[i]))
        i=i+1
def clickplus(number):
    global ticketsarray
    ticketsarray[number]+=1
    AmountOfTicketsLabel[number].configure(text=ticketsarray[number])
    CalTotalCost()
def clickminus(number):
    global ticketsarray
    if ticketsarray[number]>0:
        ticketsarray[number]-=1
        AmountOfTicketsLabel[number].configure(text=ticketsarray[number])
    CalTotalCost()
def CalTotalCost():
    global TotalCostZl
    TotalCostZl=0
    for i in range(len(ticketsarray)):
        TotalCostZl+=ticketsarray[i]*TicketsPrices[i]
    TotalCost.configure(text=str("%.2f" %TotalCostZl)+'zl')
def close_window():
    window.destroy()
    exit()

GetTicketsPrices()
CreateLabels()
TotalCost=Label(window,width=8,text=str(TotalCostZl)+'zl')
Button(window,text="Zakoncz",width=20,command=close_window).grid(row =9, column=0,sticky=W)
Button(window,text="Platnosc",width=20,command=close_window).grid(row =9, column=5, sticky=E)
TotalCost.grid(column=5,row = 8)
window.mainloop()
conn.commit()
conn.close()