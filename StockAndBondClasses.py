"""
This module contains classes for stocks and bonds
along with the necessary methods for them
------------------------------------------------------------
ICT-4730-1 Python Programming
Stock and Bonds Classes
Abby Smith
8/21/2022
"""

# Importing necessary functions
import datetime as dt
import itertools


class Investor:
    new_investor_id = itertools.count(1, 1)

    def __init__(self, first_name, last_name, address, phone_num):
        self.first_name = first_name
        self.last_name = last_name
        self. address = address
        self.phone_num = phone_num
        self.stock_list = []
        self.bond_list = []
        self.investor_id = next(self.new_investor_id)

    # Method to get investor ID
    def get_investor_id(self):
        return self.investor_id

    # Method to get stocks and add to list
    def add_stock(self, stock):
        self.stock_list.append(stock)

    # Method to get bond(s) and add to list
    def add_bond(self, bond):
        self.bond_list.append(bond)

    # Method to return stock list
    def return_stock_list(self):
        return self.stock_list

    # Method to return bond list
    def return_bond_list(self):
        return self.bond_list


# Defining stock class
class Stock:

    # Creating stock ID using itertools library
    new_stock_id = itertools.count(0, 1)

    def __init__(self, stock_id, stock_symbol, total_shares, purchase_price, current_price, purchase_date):
        self.stock_id = stock_id
        self.stock_symbol = stock_symbol
        self.total_shares = total_shares
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.purchase_date = purchase_date
        self.current_values = []
        self.current_prices = []
        self.purchase_dates = []

    def add_current_price(self, price):
        self.current_prices.append(price)

    def add_purchase_date(self, date):
        self.purchase_dates.append(date)

    # Returns new stock id
    def get_stock_id(self):
        self.stock_id = next(self.new_stock_id)
        return self.stock_id

    def current_value(self):
        for price in self.current_prices:
            stock_value = float(("{:.2f}".format(price * self.total_shares)))
            self.current_values.append(stock_value)
        return self.current_values

    # Method to calculate stock gains and losses
    def gain_loss_calc(self, stock):
        try:
            # Initializing variables for loop
            gain_loss_value = 0
            gain_counter = 0
            loss_counter = 0
            # Looping through lists to calculate gains/losses
            if stock.current_price > stock.purchase_price:
                gain_loss_value = ("{:.2f}".format(((float(stock.current_price) * int(stock.total_shares))
                               - (float(stock.purchase_price) * int(stock.total_shares)))))
                gain_counter += 1
            elif stock.current_price < stock.purchase_price:
                gain_loss_value = ("{:.2f}".format(((float(stock.current_price) * int(stock.total_shares))
                               - (float(stock.purchase_price) * int(stock.total_shares)))))
                loss_counter += 1
            return gain_loss_value, gain_counter, loss_counter
        except TypeError:
            print('Cannot do mathematical operations on type: STR')
            print('Convert STR values from file to INT or FLOAT.\n')

    # Method to get current gain/loss percentage
    def gain_loss_percentage(self, stock):
        try:
            # Looping through list to get percentages
            percent_yield = "{:.2f}".format((((float(stock.current_price) - float(stock.purchase_price)) /
                                               float(stock.purchase_price)) * 100))
            return percent_yield
        # If the datatypes from the file are not converted this exception will fire.
        except TypeError:
            print('Cannot do mathematical operations on type: STR')
            print('Convert STR values from file to INT or FLOAT.\n')

    # Method to get yearly gain/loss percentage
    def yearly_gain_loss_percentage(self, stock):
        try:
            # Initializing list to hold yearly yields and the current date value
            import datetime as dt
            date_split = []
            current_date = dt.date.today()
            date_split = stock.purchase_date.split('/')
            purchase_date = dt.date(int(date_split[2]), int(date_split[0]), int(date_split[1]))
            # Looping through list to get percentages
            yearly_factor = (current_date - purchase_date).days / 365
            percent_yield = ("{:.2f}".format((((float(stock.current_price)
                                                - float(stock.purchase_price)) / float(stock.purchase_price)) /
                                                yearly_factor) * 100))
            return percent_yield
        # If the datatypes from the file are not converted this exception will fire.
        except TypeError:
            print('Cannot do mathematical operations on type: STR')
            print('Convert STR values from file to INT or FLOAT.\n')


class Bond(Stock):
    # getting new id for bond
    new_bond_id = itertools.count(1, 1)

    def __init__(self, stock_id, stock_symbol, total_shares, purchase_price, current_price, purchase_date,
                 coupon, percent_yield):
        super().__init__(stock_id, stock_symbol, total_shares, purchase_price, current_price, purchase_date)
        self. coupon = coupon
        self.percent_yield = percent_yield

    # Returns a new bond id
    def get_bond_id(self):
        self.stock_id = next(self.new_bond_id)
        return self.stock_id

