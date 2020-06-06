"""
    Projekt JS
    Informatyka PK semestr 4
        Automat Biletowy MPK

"""
import sys
import sqlite3
import tkinter as tk

DATABASE_NAME = 'automat.db'
NOMINAL = 2
NUMBER_OF_COINS = 1
TICKET_NAME = 0
TICKET_PRICE = 1
VALUE_IN_GR = 0


class AvailableCash():  # pylint: disable=too-few-public-methods
    """
    Available cash that is in machine for change
    """

    def __init__(self):
        """
        init a element that have own value in grosz and amount of it
        """
        self.value_in_gr = 0
        self.number_of_coins = 0


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
        self.total_cost_zl_main = tk.DoubleVar()
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
        self.total_cost_zl_main.set(f"{(self.total_cost_main.get() / 100.0):.2f} zł")
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
                self.destroy()
                MainWindow().mainloop()

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
        self.total_cost_zl = controller.total_cost_main
        self.tickets = [tk.IntVar() for _ in range(6)]
        self.labels = []
        self.tickets_labels = []
        self.tickets_prices = []
        self.total_cost = tk.Label(self, width=8, text=f"{self.total_cost_zl} zł")
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

    def on_change(self, first_arg=None, second_arg=None, thrird_arg=None):
        """
        When entry value change it also change a variable value
        and check if entry value is greater than 0
        :return: no return
        """
        del first_arg, second_arg, thrird_arg
        temp = None
        for ticket, label in zip(self.tickets, self.tickets_labels):
            try:
                temp = ticket.get()
            except tk.TclError:
                ticket.set(0)
            else:
                if temp < 0:
                    ticket.set(0)
                label.update_idletasks()
        self.tickets_labels[-1].update_idletasks()
        self.count_total_cost()

    def create_labels(self):
        """
        creating a labels for TicketSelect frame
        :return: no return
        """
        del self.labels[:]
        del self.tickets_labels[:]
        del self.tickets[:]
        conn = sqlite3.connect(DATABASE_NAME)
        coins_cursor = conn.cursor()
        i = 0
        for nazwa, cena in coins_cursor.execute(
                """SELECT nazwa,cena FROM bilety ORDER BY Id_biletu"""
        ):
            ticket = tk.IntVar()
            ticket.set(0)
            self.labels.append(tk.Label(
                self, text=f"{nazwa} {cena / 100:.2f} zł"
            ))
            self.labels[i].grid(column=0, row=i + 2, pady=15)
            temp_entry = tk.Entry(self, justify=tk.CENTER, command=self.count_total_cost(),
                                  text="0", width=5,
                                  textvariable=ticket)
            self.tickets_labels.append(temp_entry)
            self.tickets_labels[i].grid(column=4, row=i + 2, pady=15)
            plus_button = tk.Button(self, text="+", width=4, command=lambda j=i: self.click_plus(j))
            plus_button.grid(row=i + 2, column=3, sticky=tk.W)
            minus_button = tk.Button(self, text="-", width=4,
                                     command=lambda j=i: self.click_minus(j))
            minus_button.grid(row=i + 2, column=5, sticky=tk.W)
            ticket.trace("w", self.on_change)
            self.tickets.append(ticket)
            i += 1

    def get_tickets_prices(self):
        """
        used to get tickets prices from database and append them to tickets_prices list
        :return: no return
        """
        del self.tickets_prices[:]
        conn = sqlite3.connect(DATABASE_NAME)
        p_cursor = conn.cursor()
        for row in p_cursor.execute('SELECT cena FROM bilety ORDER BY Id_biletu'):
            self.tickets_prices.append(row[0])

    def click_plus(self, number):
        """
        increase by 1 amount of tickets
        :param number: Ticket number
        :return:
        """
        temp = self.tickets[number].get()
        self.tickets[number].set(temp + 1)
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
        self.count_total_cost()

    def count_total_cost(self):
        """
        calculates the total price for selected tickets
        :return:
        """
        cost_zl = 0.0
        for ticket, price in zip(self.tickets, self.tickets_prices):
            cost_zl += ticket.get() * price
        self.total_cost_zl.set(cost_zl)
        self.total_cost.configure(text=f"{(cost_zl / 100):.2f} zl")

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
        self.number_of_coins = []
        self.menu_buttons = []
        self.how_many_coins = tk.IntVar()
        self.how_many_coins.set(1)
        self.total_cash = tk.DoubleVar()
        self.total_cost = controller.total_cost_main
        self.total_cost_zl = controller.total_cost_zl_main
        self.to_pay = tk.Label(self, font="Helvetica 14 bold", textvariable=self.total_cost_zl)
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
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        i = 0
        j = 0
        for value_gr, nominal in cursor.execute(
                """SELECT monety.wartosc_w_gr,monety.nominal
                FROM monety
                ORDER BY monety.wartosc_w_gr DESC"""
        ):
            temp_button = tk.Button(self, text=f"{nominal}", width=8, height=3,
                                    command=lambda t=int(value_gr): self.add_coin(t))
            temp_button.grid(row=j, column=i, sticky=tk.W, pady=5, padx=5)
            self.menu_buttons.append(temp_button)
            i += 1
            if i % 3 == 0:
                j += 1
                i = 0
        i = 0
        for value_gr, nominal in cursor.execute(
                """SELECT banknoty.wartosc_w_gr,banknoty.nominal
                FROM banknoty
                ORDER BY banknoty.wartosc_w_gr DESC"""
        ):
            temp_button = tk.Button(self, text=f"{nominal}", width=8, height=3,
                                    command=lambda t=int(value_gr): self.add_coin(t))
            temp_button.grid(row=j, column=i, sticky=tk.W, pady=5, padx=5)
            self.menu_buttons.append(temp_button)

            i += 1
            tk.Label(self, text="Ile monet chcesz wrzucić? ").grid(row=0, column=4)
            tk.Entry(self, width=8, justify=tk.CENTER,
                     textvariable=self.how_many_coins).grid(row=1, column=4)

    def add_coin(self, coin_value_gr):
        """
        add selected coin to our machine
        :param coin_value_gr: type of coin
        :return:
        """
        try:
            if coin_value_gr <= 0:
                raise ValueError()
        except ValueError:
            print(f" Nie ma monety o wartosci: {coin_value_gr / 100}  zł")
        else:
            for _ in range(0, self.how_many_coins.get()):
                self.number_of_coins.append(coin_value_gr)
            self.total_cash.set(sum(self.number_of_coins))
            if self.total_cash.get() >= self.total_cost.get():
                self.pay()
            self.in_machine.configure(text=
                                      f"Wrzucono już: {(sum(self.number_of_coins) / 100):.2f} zł"
                                      )

    def pay(self):
        """
        End of payment if we threw in enough coins,
        if thats true count and give a change,
        and add thrown in coins to our machine (increase Ilosc in database)
        :return:
        """
        if self.total_cash.get() < self.total_cost.get():
            self.controller.warning("Wrzuciłeś za mało piniędzy")
        else:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            self.records_amount = cursor.execute(
                """
                SELECT ((SELECT COUNT(*) FROM Monety) +
                (SELECT COUNT(*) FROM Banknoty))
                """
            ).fetchone()[0]
            # DO TESTU
            # self.records_amount = cursor.execute("""
            # select count(*) from Monety,Banknoty
            # """
            # ).fetchone()[0]
            available_cash = [AvailableCash() for _ in range(self.records_amount)]
            i = 0
            for row in cursor.execute(
                    """SELECT banknoty.wartosc_w_gr, banknoty.ilosc
                    FROM banknoty
                    ORDER BY banknoty.wartosc_w_gr DESC"""
            ):
                available_cash[i].value_in_gr = row[VALUE_IN_GR]
                available_cash[i].number_of_coins = row[NUMBER_OF_COINS]
                i += 1
            for row in cursor.execute(
                    """SELECT monety.wartosc_w_gr,monety.ilosc
                    FROM monety
                    ORDER BY monety.wartosc_w_gr DESC"""
            ):
                available_cash[i].value_in_gr = row[VALUE_IN_GR]
                available_cash[i].number_of_coins = row[NUMBER_OF_COINS]
                i += 1
            for i in self.number_of_coins:
                for j, _ in enumerate(available_cash):
                    if i == available_cash[j].value_in_gr:
                        available_cash[j].number_of_coins += 1
                        break
            change = self.total_cash.get() - self.total_cost.get()
            change_temp = change
            i = 0
            while change > 0:
                if available_cash[i].value_in_gr <= change:
                    temp = change // available_cash[i].value_in_gr
                    change -= (available_cash[i].value_in_gr * temp)
                    available_cash[i].number_of_coins -= 1
                else:
                    i += 1
            self.update_database(available_cash)
            self.controller.warning(f"Dziękujemy za zakup \n Wydano:"
                                    f" {(change_temp / 100.):.2f} zł", 1)

    def update_database(self, cash):
        """
        function responsible for update amount of cash in our database
        :param cash: all cash throwed into machine in current transactions
        :return: no return
        """
        conn = sqlite3.connect(DATABASE_NAME)
        bills_amount = conn.cursor().execute(
            """
                SELECT COUNT(*) FROM Banknoty
            """
        ).fetchone()[0] + 1
        p_cursor = conn.cursor()
        for i, row in enumerate(cash):
            if i < bills_amount:
                p_cursor.execute("""UPDATE banknoty SET ilosc=?
                                WHERE wartosc_w_gr=?""",
                                 (row.number_of_coins, row.value_in_gr)
                                 )
            else:
                p_cursor.execute("""UPDATE monety
                                SET ilosc=?
                                WHERE wartosc_w_gr=?""",
                                 (row.number_of_coins, row.value_in_gr))
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
