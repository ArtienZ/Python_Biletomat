import sqlite3
import tkinter as tk
import unittest

import main

DATABASE_NAME = 'automat.db'
TICKET_PRICE = 1
"""
test main module
testing Payment class and TicketSelect class
"""


class Controller():
    def __init__(self):
        self.total_cost_zl_main = tk.DoubleVar()
        self.total_cost_main = tk.DoubleVar()

    def warning(self, a, b):
        print("ITS WARRNING")
        print(a)


class TestPayment(unittest.TestCase):
    def setUp(self):
        self.ts = main.Payment(tk.Frame(), Controller())

    def test_add_coin(self):
        self.ts.total_cost.set(10000)
        self.ts.add_coin(1000)
        self.assertEqual(self.ts.number_of_coins[-1], 1000)
        self.ts.add_coin(1)
        self.assertEqual(self.ts.number_of_coins[-1], 1)
        self.ts.add_coin(-100)
        self.ts.add_coin(100)
        self.assertNotIn(-100, self.ts.number_of_coins)

    def test_pay(self):
        self.number_of_denominations = 12
        self.ts.total_cash.set(10000)
        self.ts.total_cost.set(1000)
        self.ts.pay()
        self.assertEqual(self.ts.records_amount, self.number_of_denominations)
        self.ts.total_cash.set(0)
        self.ts.total_cost.set(0)

    def test_pay_odliczona_kwota(self):
        self.ts.total_cost.set(1000)
        self.ts.total_cash.set(1000)
        self.ts.pay()
        self.assertEqual(self.ts.change_temp, 0)

    def test_pay_placac_wiecej(self):
        self.ts.total_cost.set(2000)
        self.ts.add_coin(5000)
        self.ts.pay()
        self.assertEqual(self.ts.change_temp, 3000)

    def test_pay_1gr(self):
        self.ts.total_cost.set(100)
        for _ in range(0, 100):
            self.ts.add_coin(1)
        self.ts.pay()
        self.assertEqual(self.ts.change, 0)


class TestTicketSelect(unittest.TestCase):
    def setUp(self):
        self.ts = main.TicketSelect(tk.Frame(), Controller())

    def test_get_tickets_prices(self):

        self.ts.get_tickets_prices()
        conn = sqlite3.connect(DATABASE_NAME)
        for row in conn.cursor().execute(
                'SELECT nazwa, cena FROM bilety ORDER BY Id_biletu'
        ):
            self.assertIn(row[TICKET_PRICE], self.ts.tickets_prices)

    def test_click_plus(self):
        for i, value in enumerate(self.ts.tickets):
            self.ts.click_plus(i)
            self.assertEqual(value.get(), 1)

    def test_click_minus(self):
        for i, value in enumerate(self.ts.tickets):
            self.ts.click_minus(i)
            self.assertEqual(value.get(), 0)
        self.ts.tickets[0].set(10)
        self.ts.click_minus(0)
        self.assertEqual(self.ts.tickets[0].get(), 9)

    def test_count_total_cost(self):
        self.ts.tickets[0].set(10)
        self.ts.count_total_cost()
        self.assertEqual(self.ts.total_cost_zl.get(), 7500)

    def test_two_diff_tickets(self):
        self.ts.tickets[0].set(1)
        self.ts.tickets[1].set(1)
        self.ts.count_total_cost()
        self.assertEqual(self.ts.total_cost_zl.get(), 2250)


if __name__ == '__main__':
    unittest.main()
