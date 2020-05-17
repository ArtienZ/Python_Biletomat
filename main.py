"""
    Projekt JS
    Informatyka PK semestr 4
        Automat Biletowy MPK

"""
import sqlite3
import tkinter
import sys


def warning(msg, option=0):
    """

    :param msg: The text of popup warning.
    :param option: Warning option default 0.
    :return: Create a new popup window and making inactive mainwindow
    """
    popup = tkinter.Tk()
    APP_GUI.withdraw()

    def leave_war():
        """
        When window option set to 0 just destroying this window and making active a mainwindow,
        if set to 1 destroy this window and mainwindow
        :return: no return
        """
        if option == 0:
            popup.destroy()
            APP_GUI.deiconify()
        else:
            popup.destroy()
            APP_GUI.destroy()

    popup.wm_title("POWIADOMIENIE ")
    label = tkinter.Label(popup, text=msg, font="Helvetica 20 bold")
    label.pack(side="top", fill='x', pady=10)
    go_back = tkinter.Button(popup, text="Powrót", font="Helvetica 16", command=leave_war)
    go_back.pack()
    popup.mainloop()


class MainWindow(tkinter.Tk):
    """
    class for mainwindow of biletomat
    """

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.geometry("600x400")
        self.title("Automat biletowy MPK")
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.app_data = {"total_cost": tkinter.DoubleVar(),
                         "total_costzl": tkinter.DoubleVar()
                         }
        # frame=TicketSelect(container,self)
        # frame.grid(row=0, column=0, sticky="nsew")
        # self.frames[TicketSelect]=frame
        # frame=Payment(container,self)
        # frame.grid(row=0, column=0, sticky="nsew")
        # self.frames[Payment]=frame
        self.frames = {}
        for frame_name in (TicketSelect, Payment):
            frame = frame_name(container, self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(TicketSelect)

    def show_frame(self, cont):
        """
        move to other frame
        :param cont: containter name
        :return: no return
        """
        self.app_data["total_costzl"].set(f"{'%.2f' % (self.app_data['total_cost'].get() / 100.0)} zł")
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        """

        :param page_class: name of page
        :return: frame of this page
        """
        return self.frames[page_class]


class TicketSelect(tkinter.Frame):
    """
    1st frame of app
    menu with tickets
    """

    def __init__(self, parent, controller):
        """

        :param parent: parent window
        :param controller: controller used to move between frames
        """
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.total_costzl = self.controller.app_data["total_cost"]
        self.tickets = [tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(),
                        tkinter.IntVar()]
        self.labels = []
        self.tickets_labels = []
        self.tickets_prices = []
        self.conn = sqlite3.connect('automat.db')
        self.total_cost = tkinter.Label(self, width=8, text=f"{self.total_costzl} zł")
        self.get_tickets_prices()
        self.create_labels()
        close_program = tkinter.Button(self, text="Zakoncz", width=20, command=self.close_frame)
        close_program.grid(row=9, column=0,
                           sticky=tkinter.W)
        go_to_payment = tkinter.Button(self, text="Platnosc", width=20, command=lambda: controller.show_frame(Payment))
        go_to_payment.grid(row=9,
                           column=5,
                           sticky=tkinter.E)
        self.total_cost.grid(column=5, row=8)
        self.conn.commit()

    def on_change(self, a=None, b=None, c=None):
        """
        When entry value change it also change a variable value
        and check if entry value is greater than 0
        :param a:
        :param b:
        :param c:
        :return: no return
        """
        for k in range(0, len(self.tickets)):
            try:
                temp = self.tickets[k].get()
            except:
                self.tickets[k].set(0)
            if temp < 0:
                self.tickets[k].set(0)
            self.tickets_labels[k].update_idletasks()
        self.tickets_labels[k].update_idletasks()
        self.cal_total_cost()

    def create_labels(self):
        """
        creating a labels for TicketSelect frame
        :return: no return
        """
        del self.labels[:]
        del self.tickets_labels[:]
        del self.tickets[:]
        print(len(self.tickets))
        self.coins_cursor = self.conn.cursor()
        self.coins_cursor.execute('SELECT nazwa,cena FROM bilety ORDER BY Id_biletu')
        records = self.coins_cursor.fetchall()
        self.i = 0
        for row in records:
            self.tickets.append(tkinter.IntVar())
            self.tickets[self.i].set(0)
            self.labels.append(tkinter.Label(self, text=f"{row[0]} {row[1] / 100:.2f} zł"))
            self.labels[self.i].grid(column=0, row=self.i + 2, pady=15)
            self.tickets_labels.append(
                tkinter.Entry(self, justify=tkinter.CENTER, command=self.cal_total_cost(), text="0", width=5,
                              textvariable=self.tickets[self.i]))
            self.tickets_labels[self.i].grid(column=4, row=self.i + 2, pady=15)
            plus_button = tkinter.Button(self, text="+", width=4, command=lambda i=self.i: self.click_plus(i))
            plus_button.grid(row=self.i + 2, column=3, sticky=tkinter.W)
            minus_button = tkinter.Button(self, text="-", width=4, command=lambda i=self.i: self.click_minus(i))
            minus_button.grid(row=self.i + 2, column=5, sticky=tkinter.W)
            self.tickets[self.i].trace("w", self.on_change)
            self.i = self.i + 1

    def get_tickets_prices(self):
        """
        used to get tickets prices from database and append them to tickets_prices list
        :return: no return
        """
        del self.tickets_prices[:]
        p_cursor = self.conn.cursor()
        p_cursor.execute('SELECT cena FROM bilety ORDER BY Id_biletu')
        records = p_cursor.fetchall()
        for row in records:
            self.tickets_prices.append(row[0])

    def click_plus(self, number):
        """
        increase by 1 amount of tickets
        :param number: Ticket number
        :return:
        """
        temp = self.tickets[number].get()
        self.tickets[number].set(temp + 1)
        # self.tickets_labels[number].delete(0, END)
        # self.tickets_labels[number].insert(0, self.tickets[number].get())
        self.cal_total_cost()

    def click_minus(self, number):
        """
        decreases by 1 amount of tickets only if its greater than 0
        :param number: Ticket number
        :return:
        """
        temp = self.tickets[number].get()
        if temp > 0:
            self.tickets[number].set(temp - 1)
            # self.tickets_labels[number].delete(0,END)
            # self.tickets_labels[number].insert(0,self.tickets[number].get())
        self.cal_total_cost()

    def cal_total_cost(self):
        """
        calculates the total price for selected tickets
        :return:
        """
        temp = 0.0
        for j in range(len(self.tickets)):
            temp += self.tickets[j].get() * self.tickets_prices[j]
        self.total_costzl.set(temp)
        self.total_cost.configure(text=f"{str('%.2f' % (float(self.total_costzl.get()) / 100))} zl")

    def close_frame(self):
        """
        destroy specific frame
        :return:
        """
        self.master.destroy()
        sys.exit()


class Payment(tkinter.Frame):
    """
    Payment for selected tickets
    """

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.conn = sqlite3.connect('automat.db')
        self.amount_of_coins = []
        self.menu_buttons = []
        self.how_many_coins = tkinter.IntVar()
        self.how_many_coins.set(1)
        self.total_cash = tkinter.DoubleVar()
        self.total_cost = self.controller.app_data["total_cost"]
        self.total_costzl = self.controller.app_data["total_costzl"]
        self.coins_in = []
        self.to_pay = tkinter.Label(self, font="Helvetica 14 bold", textvariable=self.total_costzl)
        self.in_machine = tkinter.Label(self, font="Helvetica 14 bold", text="Wrzucono już: 0.0 zł")
        self.coin_menu()
        tkinter.Button(self, text="Zakończ", width=8, command=self.close_frame).grid(row=9, column=0)
        tkinter.Button(self, text="Zapłać", width=8, command=self.pay).grid(row=9, column=1)
        tkinter.Button(self, text="Powrót", width=8, command=lambda: controller.show_frame(TicketSelect)).grid(row=9,
                                                                                                               column=5)
        self.to_pay.grid(row=2, column=4)
        self.in_machine.grid(row=3, column=4)

    def coin_menu(self):
        """
        Creating a menu of all coins that are able in our biletomat database
        :return:
        """

        self.coins_cursor = self.conn.cursor()
        self.note_cursor = self.conn.cursor()
        self.coins_cursor.execute(
            "SELECT monety.nominal,monety.ilosc,monety.wartosc_w_gr FROM monety ORDER BY monety.wartosc_w_gr DESC")
        self.note_cursor.execute(
            "SELECT banknoty.nominal,banknoty.ilosc,banknoty.wartosc_w_gr FROM banknoty ORDER BY banknoty.wartosc_w_gr DESC")
        self.records_coins = self.coins_cursor.fetchall()
        self.records_notes = self.note_cursor.fetchall()
        i = 0
        j = 0
        for res in self.records_coins:
            self.menu_buttons.append(
                tkinter.Button(self, bg='lightgray', command=lambda t=int(res[2]): self.add_coin(t), text=f"{res[0]}",
                               width=8,
                               height=3).grid(row=j, column=i, sticky=tkinter.W, pady=5, padx=5))
            i += 1
            if i % 3 == 0:
                j += 1
                i = 0
        i = 0
        for res in self.records_notes:
            self.menu_buttons.append(
                tkinter.Button(self, bg='lightgray', command=lambda t=int(res[2]): self.add_coin(t), text=f"{res[0]}",
                               width=8,
                               height=3).grid(row=j, column=i, sticky=tkinter.W, pady=5, padx=5))
            i += 1
        tkinter.Label(self, font="Helvetica 14", text="Ile monet chcesz wrzucić? ").grid(row=0, column=4)
        tkinter.Entry(self, width=8, font="Helvetica 14 bold", justify=tkinter.CENTER,
                      textvariable=self.how_many_coins).grid(row=1, column=4)

    def add_coin(self, coin_type):
        """
        add selected coin to our machine
        :param coin_type: type of coin
        :return:
        """
        for i in range(0, self.how_many_coins.get()):
            self.amount_of_coins.append(coin_type)
        self.total_cash.set(sum(self.amount_of_coins))
        self.in_machine.configure(text=f"Wrzucono już: {'%.2f' % (sum(self.amount_of_coins) / 100)} zł")

    def pay(self):
        """
        End of payment if we threw in enough coins,
        if thats true calc and give a change and add thrown in coins to our machine (increase Ilosc in database)

        :return:
        """
        if self.total_cash.get() < self.total_cost.get():
            warning("Wrzuciłeś za małą kwotę")
        else:
            avalible_cash = [[0 for x in range(2)] for y in range(len(self.records_notes) + len(self.records_coins))]
            i = 0
            for row in self.records_notes:
                avalible_cash[i][0] = row[2]
                avalible_cash[i][1] = row[1]
                i += 1
            for row in self.records_coins:
                avalible_cash[i][0] = row[2]
                avalible_cash[i][1] = row[1]
                i += 1
            print(avalible_cash)
            for i in self.amount_of_coins:
                for j in range(0, len(avalible_cash)):
                    if i == avalible_cash[j][0]:
                        avalible_cash[j][1] += 1
                        break
            change = self.total_cash.get() - self.total_cost.get()
            change_temp = change
            i = 0
            while change > 0:
                if avalible_cash[i][0] <= change:
                    temp = change // avalible_cash[i][0]
                    change -= (avalible_cash[i][0] * temp)
                    avalible_cash[i][1] -= 1
                    print(f"{avalible_cash[i][0]} {temp} {change}")
                else:
                    i += 1
            print(avalible_cash)
            print(change)
            p_cursor = self.conn.cursor()
            i = 0
            for denom, amout in avalible_cash:
                print(len(self.records_notes))
                print(f"{denom}    {amout}")
                if i < len(self.records_notes):
                    p_cursor.execute("""UPDATE banknoty SET ilosc=? WHERE wartosc_w_gr=?""", (amout, denom))
                else:
                    p_cursor.execute("""UPDATE monety SET ilosc=? WHERE wartosc_w_gr=?""", (amout, denom))
                i += 1
            self.conn.commit()
            print(f"Wrzucone monety {self.amount_of_coins} kwota:{sum(self.amount_of_coins)}")
            warning(f"Dziękujemy za zakup \n Wydano: {'%.2f' % (change_temp / 100.)}", 1)

    def close_frame(self):
        """
        close frame
        :return:
        """
        self.master.destroy()
        sys.exit()


APP_GUI = MainWindow()
APP_GUI.mainloop()
