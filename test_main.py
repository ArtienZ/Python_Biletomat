import unittest
import main
import sqlite3
import tkinter as tk

TICKET_PRICE = 1
"""
test main module
testing Payment class and TicketSelect class
"""

class Controller():
    def __init__(self):
        self.total_costzl_main = tk.DoubleVar()
        self.total_cost_main = tk.DoubleVar()


class test_Main(unittest.TestCase):
    def test_add_coin(self):

        temp = main.Payment(tk.Frame(), Controller())
        temp.total_cost.set(10000)
        temp.add_coin(1000)
        self.assertEqual(temp.amount_of_coins[-1], 1000)
        temp.add_coin(1)
        self.assertEqual(temp.amount_of_coins[-1], 1)
        temp.add_coin(-100)
        temp.add_coin(100)
        self.assertNotIn(-100, temp.amount_of_coins)

    def test_get_tickets_prices(self):
        temp = main.TicketSelect(tk.Frame(), Controller())
        temp.get_tickets_prices()
        conn = sqlite3.connect('automat.db')
        for row in conn.cursor().execute(
                'SELECT nazwa, cena FROM bilety ORDER BY Id_biletu'
        ):
            self.assertIn(row[TICKET_PRICE], temp.tickets_prices)

    def test_click_plus(self):
        temp = main.TicketSelect(tk.Frame(), Controller())
        for i, value in enumerate(temp.tickets):
            temp.click_plus(i)
            self.assertEqual(value.get(), 1)

    def test_click_minus(self):
        temp = main.TicketSelect(tk.Frame(), Controller())
        for i, value in enumerate(temp.tickets):
            temp.click_minus(i)
            self.assertEqual(value.get(), 0)
        temp.tickets[0].set(10)
        temp.click_minus(0)
        self.assertEqual(temp.tickets[0].get(), 9)

    def test_count_total_cost(self):
        temp = main.TicketSelect(tk.Frame(), Controller())
        temp.tickets[0].set(10)
        temp.count_total_cost()
        self.assertEqual(temp.total_costzl.get(), 7500)


if __name__ == '__main__':
    unittest.main()
