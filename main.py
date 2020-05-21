"""
    Projekt JS
    Informatyka PK semestr 4
        Automat Biletowy MPK

"""
import sqlite3
import tkinter as tk
import sys


class MainWindow(tk.Tk):
    """
    class for mainwindow of biletomat
    """

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("600x400")
        self.title("Automat biletowy MPK")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.total_cost_main = tk.DoubleVar()
        self.total_costzl_main = tk.DoubleVar()
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
        self.total_costzl_main.set(f"{(self.total_cost_main.get() / 100.0):.2f} zł")
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        """

        :param page_class: name of page
        :return: frame of this page
        """
        return self.frames[page_class]

    def warning(self, msg, option=0):
        """

        :param msg: The text of popup warning.
        :param option: Warning option default 0.
        :return: Create a new popup window and making inactive mainwindow
        """
        popup = tk.Tk()
        self.withdraw()

        def destroy_warning(window):
            """
            When window option set to 0 just destroying this window and making active a mainwindow,
            if set to 1 destroy this window and mainwindow
            :return: no return
            """
            if option == 0:
                popup.destroy()
                window.deiconify()
            else:
                popup.destroy()
                window.destroy()

        popup.wm_title("POWIADOMIENIE ")
        label = tk.Label(popup, text=msg, font="Helvetica 20 bold")
        label.pack(side="top", fill='x', pady=10)
        go_back = tk.Button(popup, text="Powrót", font="Helvetica 16",
                            command=lambda w=self: destroy_warning(w))
        go_back.pack()
        popup.mainloop()


class TicketSelect(tk.Frame):  # pylint: disable=too-many-ancestors
    """
    1st frame of app
    menu with tickets
    """

    def __init__(self, parent, controller):
        """

        :param parent: parent window
        :param controller: controller used to move between frames
        """
        tk.Frame.__init__(self, parent)
        self.total_costzl = controller.total_cost_main
        self.tickets = [tk.IntVar(),
                        tk.IntVar(),
                        tk.IntVar(),
                        tk.IntVar(),
                        tk.IntVar(),
                        tk.IntVar()]
        self.labels = []
        self.tickets_labels = []
        self.tickets_prices = []
        # self.conn = sqlite3.connect('automat.db')
        self.total_cost = tk.Label(self, width=8, text=f"{self.total_costzl} zł")
        self.get_tickets_prices()
        self.create_labels()
        tk.Button(self, text="Zakoncz", width=20, command=self.close_frame).grid(row=9,
                                                                                 column=0,
                                                                                 sticky=tk.W)
        go_to_payment = tk.Button(self, text="Platnosc", width=20,
                                  command=lambda: controller.show_frame(Payment))
        go_to_payment.grid(row=9,
                           column=5,
                           sticky=tk.E)
        self.total_cost.grid(column=5, row=8)
        # self.conn.commit()

    def on_change(self, first_arg=None, second_arg=None, thrird_arg=None):
        """
        When entry value change it also change a variable value
        and check if entry value is greater than 0
        :return: no return
        """
        del first_arg, second_arg, thrird_arg
        k = 0
        temp = None
        for k, _ in enumerate(self.tickets):
            try:
                temp = self.tickets[k].get()
            except tk.TclError:
                self.tickets[k].set(0)
            else:
                if temp < 0:
                    self.tickets[k].set(0)
                self.tickets_labels[k].update_idletasks()
        self.tickets_labels[k].update_idletasks()
        self.count_total_cost()

    def create_labels(self):
        """
        creating a labels for TicketSelect frame
        :return: no return
        """
        del self.labels[:]
        del self.tickets_labels[:]
        del self.tickets[:]
        conn = sqlite3.connect('automat.db')
        print(len(self.tickets))
        coins_cursor = conn.cursor()
        coins_cursor.execute('SELECT nazwa,cena FROM bilety ORDER BY Id_biletu')
        records = coins_cursor.fetchall()
        for i, row in enumerate(records):
            self.tickets.append(tk.IntVar())
            self.tickets[i].set(0)
            self.labels.append(tk.Label(self, text=f"{row[0]} {row[1] / 100:.2f} zł"))
            self.labels[i].grid(column=0, row=i + 2, pady=15)
            temp_entry = tk.Entry(self, justify=tk.CENTER, command=self.count_total_cost(),
                                  text="0", width=5,
                                  textvariable=self.tickets[i])
            self.tickets_labels.append(temp_entry)
            self.tickets_labels[i].grid(column=4, row=i + 2, pady=15)
            plus_button = tk.Button(self, text="+", width=4, command=lambda j=i: self.click_plus(j))
            plus_button.grid(row=i + 2, column=3, sticky=tk.W)
            minus_button = tk.Button(self, text="-", width=4,
                                     command=lambda j=i: self.click_minus(j))
            minus_button.grid(row=i + 2, column=5, sticky=tk.W)
            self.tickets[i].trace("w", self.on_change)
        conn.commit()

    def get_tickets_prices(self):
        """
        used to get tickets prices from database and append them to tickets_prices list
        :return: no return
        """
        del self.tickets_prices[:]
        conn = sqlite3.connect('automat.db')
        p_cursor = conn.cursor()
        p_cursor.execute('SELECT cena FROM bilety ORDER BY Id_biletu')
        records = p_cursor.fetchall()
        for row in records:
            self.tickets_prices.append(row[0])
        conn.commit()

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
        self.count_total_cost()

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
        self.count_total_cost()

    def count_total_cost(self):
        """
        calculates the total price for selected tickets
        :return:
        """
        temp = 0.0
        for j in range(len(self.tickets)):
            temp += self.tickets[j].get() * self.tickets_prices[j]
        self.total_costzl.set(temp)
        self.total_cost.configure(text=f"{(self.total_costzl.get() / 100):.2f} zl")

    def close_frame(self):
        """
        destroy specific frame
        :return:
        """
        self.master.destroy()
        sys.exit()


class Payment(tk.Frame):  # pylint: disable=too-many-ancestors
    """
    Payment for selected tickets
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.amount_of_coins = []
        self.menu_buttons = []
        self.how_many_coins = tk.IntVar()
        self.how_many_coins.set(1)
        self.total_cash = tk.DoubleVar()
        self.total_cost = controller.total_cost_main
        self.total_costzl = controller.total_costzl_main
        self.coins_in = []
        self.to_pay = tk.Label(self, font="Helvetica 14 bold", textvariable=self.total_costzl)
        self.in_machine = tk.Label(self, font="Helvetica 14 bold", text="Wrzucono już: 0.0 zł")
        self.coin_menu()
        tk.Button(self, text="Zakończ", width=8, command=self.close_frame).grid(row=9, column=0)
        tk.Button(self, text="Zapłać", width=8, command=self.pay).grid(row=9, column=1)
        back_button = tk.Button(self, text="Powrót", width=8,
                                command=lambda: controller.show_frame(TicketSelect))
        back_button.grid(row=9, column=5)
        self.to_pay.grid(row=2, column=4)
        self.in_machine.grid(row=3, column=4)

    def coin_menu(self):
        """
        Creating a menu of all coins that are able in our biletomat database
        :return:
        """
        conn = sqlite3.connect('automat.db')
        self.coins_cursor = conn.cursor()
        self.note_cursor = conn.cursor()
        self.coins_cursor.execute(
            """SELECT monety.nominal,monety.ilosc,monety.wartosc_w_gr
            FROM monety
            ORDER BY monety.wartosc_w_gr DESC"""
        )
        self.note_cursor.execute(
            """SELECT banknoty.nominal,banknoty.ilosc,banknoty.wartosc_w_gr
            FROM banknoty
            ORDER BY banknoty.wartosc_w_gr DESC"""
        )
        self.records_coins = self.coins_cursor.fetchall()
        self.records_notes = self.note_cursor.fetchall()
        i = 0
        j = 0
        res = None
        for res in self.records_coins:
            temp_button = tk.Button(self, text=f"{res[0]}", width=8, height=3,
                                    command=lambda t=int(res[2]): self.add_coin(t))
            temp_button.grid(row=j, column=i, sticky=tk.W, pady=5, padx=5)
            self.menu_buttons.append(temp_button)
            i += 1
            if i % 3 == 0:
                j += 1
                i = 0
        i = 0
        for res in self.records_notes:
            temp_button = tk.Button(self, text=f"{res[0]}", width=8, height=3,
                                    command=lambda t=int(res[2]): self.add_coin(t))
            temp_button.grid(row=j, column=i, sticky=tk.W, pady=5, padx=5)
            self.menu_buttons.append(temp_button)

            i += 1
            tk.Label(self, text="Ile monet chcesz wrzucić? ").grid(row=0, column=4)
            tk.Entry(self, width=8, justify=tk.CENTER,
                     textvariable=self.how_many_coins).grid(row=1, column=4)
        conn.commit()

    def add_coin(self, coin_type):
        """
        add selected coin to our machine
        :param coin_type: type of coin
        :return:
        """
        for _ in range(0, self.how_many_coins.get()):
            self.amount_of_coins.append(coin_type)
        self.total_cash.set(sum(self.amount_of_coins))
        self.in_machine.configure(text=f"Wrzucono już: {(sum(self.amount_of_coins) / 100):.2f} zł")

    def pay(self):
        """
        End of payment if we threw in enough coins,
        if thats true count and give a change,
        and add thrown in coins to our machine (increase Ilosc in database)
        :return:
        """
        if self.total_cash.get() < self.total_cost.get():
            self.controller.warning("Wrzuciłeś za małą kwotę")
        else:
            temp_sum = len(self.records_notes) + len(self.records_coins)
            avalible_cash = [[0 for _ in range(2)] for _ in range(temp_sum)]
            i = 0
            for row in self.records_notes:
                avalible_cash[i][0] = row[2]
                avalible_cash[i][1] = row[1]
                i += 1
            for row in self.records_coins:
                avalible_cash[i][0] = row[2]
                avalible_cash[i][1] = row[1]
                i += 1
            for i in self.amount_of_coins:
                for j, _ in enumerate(avalible_cash):
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
            self.update_database(avalible_cash)
            self.controller.warning(f"Dziękujemy za zakup \n Wydano:"
                                    f" {(change_temp / 100.):.2f} zł", 1)

    def update_database(self, cash):
        """
        function responsible for update amount of cash in our database
        :param cash: all cash throwed into machine in current transactions
        :return: no return
        """
        conn = sqlite3.connect('automat.db')
        p_cursor = conn.cursor()
        for i, row in enumerate(cash):
            print(len(self.records_notes))
            print(f"{row[0]}    {row[1]}")
            if i < len(self.records_notes):
                p_cursor.execute("""UPDATE banknoty SET ilosc=?
                                WHERE wartosc_w_gr=?""",
                                 (row[0], row[1])
                                 )
            else:
                p_cursor.execute("""UPDATE monety
                                SET ilosc=?
                                WHERE wartosc_w_gr=?""",
                                 (row[0], row[1]))
        conn.commit()

    def close_frame(self):
        """
        close frame
        :return:
        """
        self.master.destroy()
        sys.exit()


def main():
    """
    main function
    :return: no return
    """
    app_gui = MainWindow()
    app_gui.mainloop()


if __name__ == '__main__':
    main()
