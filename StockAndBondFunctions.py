"""
This module contains all of the functions needed for the stock
calculations as well as the functions to print stock data from the
csv and json assignments we had.
------------------------------------------------------------------
ICT-4730-1 Python Programming
Stock and Bond Functions
Abby Smith
8/21/2022
"""

# Importing necessary functions
from StockAndBondClasses import *
from datetime import datetime
import pygal
import json
import sqlite3

# This function decides there was a max gain or min loss
# Then according to which scenario fits, the symbol matching the criteria
# is returned.
def max_gain_loss(g_counter, l_counter, stock_list):
    try:
        # Initializing variables for loop
        price_differences = []
        max_gain_symbol = ''
        min_loss_symbol = ''
        index = 0
        # Loop to find max gain symbol
        # If the gain counter is greater than or equal to three, symbolizing
        # a majority gain, then the loop stores all the stock price
        # differences in a list where the max function is used to find the
        # stock symbol with the maximum gain in value
        if g_counter >= 3:
            for stock in stock_list:
                price_differences.append(float(stock.current_price) - float(stock.purchase_price))
                index += 1
            max_gain = max(price_differences)
            max_gain_index = price_differences.index(max_gain)
            index = 0
            for stock in stock_list:
                if max_gain_index == index:
                    max_gain_symbol = stock.stock_symbol
                index += 1
            return ("The stock with the highest increase in value\nin your portfolio on a per-share basis is: "
                    + str(max_gain_symbol))
        # Loop to find min loss symbol
        # If the loss counter is greater than or equal to three, symbolizing
        # a majority loss, then the loop stores all the stock price
        # differences in a list where the min function is used to find the
        # stock symbol with the minimum loss in value
        elif l_counter >= 3:
            for stock in stock_list:
                price_differences.append(float(stock.purchase_price) - float(stock.current_price))
                index += 1
            min_loss = min(price_differences)
            min_loss_index = price_differences.index(min_loss)
            index = 0
            for stock in stock_list:
                if min_loss_index == index:
                    min_loss_symbol = stock.stock_symbol
                index += 1
            return ("The stock with the minimum loss in value\nin your portfolio on a per-share basis is: "
                    + str(min_loss_symbol))
    # If the datatypes from the file are not converted this exception will fire.
    except TypeError:
        print('Cannot do mathematical operations on type: STR')
        print('Convert STR values from file to INT or FLOAT.\n')

# Function to write output to the console
def write_output(stock_list, bond_list, investor):

    # Printing the stock output
    print('Stock ownership for: ' + str(investor.first_name) + " " + str(investor.last_name))
    print(f"{'Investor ID: ' + str(investor.get_investor_id()):<12}{'':<2}"
          f"{'Address: ' + investor.address:<12}"
          f"{'':<2}{'Phone Number: ' + investor.phone_num:<12}")
    # Printing line of hyphens
    print("-" * 100)
    print(f"{'Stock ID':<12}{'Symbol':<12}{'Shares':<12}{'Gain/Loss':<12}{'Current Gain/Loss %:'}"
          f"{'':<2}{'Yearly Gain/Loss %:'}")
    # Printing line of hyphens
    print("-" * 100)

    # Getting variables ready for loop
    gain_counter = 0
    loss_counter = 0

    # Looping through stock list to call functions with Stock object
    for stock in stock_list:
        # Calling class functions
        gain_loss_value, gain_value, loss_value = stock.gain_loss_calc(stock)
        percent_yield = stock.gain_loss_percentage(stock)
        yearly_percent_yield = stock.yearly_gain_loss_percentage(stock)
        # Getting gain/loss counter values
        if gain_value == 1:
            gain_counter += 1
        if loss_value == 1:
            loss_counter += 1
        # Printing stock info
        print(f"{stock.get_stock_id():<12}{stock.stock_symbol:<12}{stock.total_shares:<12}"
              f"{'$' + str(gain_loss_value):<12}{'':<5}{'%' + str(percent_yield):<17}"
              f"{'':<5}{'%' + str(yearly_percent_yield)}")

    # Printing line of hyphens
    print("-" * 100)
    # Calling max gain/loss function
    print(max_gain_loss(gain_counter, loss_counter, stock_list))

    # writing the bond output
    print('')
    print('Bond ownership for: ' + investor.first_name + " " + investor.last_name)
    print(f"{'Investor ID: ' + str(investor.get_investor_id()):<12}"
          f"{'':<2}{'Address: ' + investor.address:<12}"
          f"{'':<2}{'Phone Number: ' + investor.phone_num:<12}")
    # Printing a line of hyphens
    print("-" * 100)
    print(f"{'Bond ID':<12}{'Symbol':<12}{'Shares':<12}{'Purchase Price':<12}"
          f"{'':<3}{'Current Price:'}{'':<2}{'Coupon:'}{'':<3}{'Yield: %'}")
    # Printing a line of hyphens
    print("-" * 100)

    # Looping through bond list with bond object
    for bond in bond_list:
        print(f"{bond.get_bond_id():<12}{bond.stock_symbol:<12}{bond.total_shares:<12}"
              f"{bond.purchase_price:<12}{'':<5}{bond.current_price:<15}{'':<1}"
              f"{bond.coupon:<11}{bond.percent_yield}")

    # Printing a line of hyphens
    print("-" * 100)

def print_csv_stocks():
    investor_one = Investor('Bob', 'Smith', '5566 Gooseberry Court, Seattle, Washington 45674', '555-666-777')
    # Setting file names
    stock_file_name = 'Lesson6_Data_Stocks.csv'
    bond_file_name = 'Lesson6_Data_Bonds.csv'
    # Getting lists ready for the loop
    split = []
    all_stocks = []
    all_bonds = []

    try:
        # Trying to open the stock file
        with open(stock_file_name) as file_object:
            # Starting with second line of file
            next(file_object)
            # Splitting the lines by attribute
            for line in file_object:
                split = line.split(',')
                investor_one.add_stock(Stock(0, split[0].strip('\n'), split[1].strip('\n'), split[2].strip('\n'),
                                             split[3].strip('\n'), split[4].strip('\n')))
    # If the file doesn't exist this exception will fire
    except FileNotFoundError:
        print(stock_file_name + " doesn't exist.")
        print('Ensure that the file path is correct')

    # Exception handling for non_existing file
    try:
        # Trying to open the bonds file
        with open(bond_file_name) as file_object:
            # Starting with second line of file
            next(file_object)
            # Splitting the lines by attribute
            for line in file_object:
                split = line.split(',')
                investor_one.add_bond(Bond(0, split[0].strip('\n'), split[1].strip('\n'), split[2].strip('\n'),
                                           split[3].strip('\n'), split[4].strip('\n'), split[5].strip('\n'),
                                           split[6].strip('\n')))
    # If the file doesn't exist this exception will fire
    except FileNotFoundError:
        print(bond_file_name + " doesn't exist.")
        print('Ensure that the file path is correct.')

    # returning stock list for investments
    all_stocks = investor_one.return_stock_list()
    # returning bond list for investments
    all_bonds = investor_one.return_bond_list()
    # Calling print output function
    write_output(all_stocks, all_bonds, investor_one)

def print_json_stocks():
    json_file = 'AllStocks.json'
    new_stock = Stock(0, '', 0, 0.00, 0.00, '')
    stock_dict = {}
    dates = []

    # Trying to open JSON file and loading it into a variable for reading
    try:
        with open(json_file) as json_object:
            data_set = json.load(json_object)

        for stock in data_set:

            # Adding dates for the graph
            if stock['Date'] not in dates:
                dates.append(stock['Date'])

            # Going through the stocks in the file and adding to dictionary
            if stock['Symbol'] not in stock_dict:
                # Depending on the symbol, there is a specific number of shares that will be assigned
                if stock['Symbol'] == 'AIG':
                    if stock['Open'] == '-':
                        new_stock = Stock(0, stock['Symbol'], 235, 0, stock['Close'], stock['Date'])
                        stock_dict[stock['Symbol']] = new_stock
                    else:
                        new_stock = Stock(0, stock['Symbol'], 235, stock['Open'], stock['Close'], stock['Date'])
                        stock_dict[stock['Symbol']] = new_stock

                elif stock['Symbol'] == 'GOOG':
                    new_stock = Stock(0, stock['Symbol'], 125, stock['Open'], stock['Close'], stock['Date'])
                    stock_dict[stock['Symbol']] = new_stock

                elif stock['Symbol'] == 'FB':
                    new_stock = Stock(0, stock['Symbol'], 150, stock['Open'], stock['Close'], stock['Date'])
                    stock_dict[stock['Symbol']] = new_stock

                elif stock['Symbol'] == 'F':
                    new_stock = Stock(0, stock['Symbol'], 85, stock['Open'], stock['Close'], stock['Date'])
                    stock_dict[stock['Symbol']] = new_stock

                elif stock['Symbol'] == 'IBM':
                    new_stock = Stock(0, stock['Symbol'], 80, stock['Open'], stock['Close'], stock['Date'])
                    stock_dict[stock['Symbol']] = new_stock

                elif stock['Symbol'] == 'M':
                    new_stock = Stock(0, stock['Symbol'], 425, stock['Open'], stock['Close'], stock['Date'])
                    stock_dict[stock['Symbol']] = new_stock

                elif stock['Symbol'] == 'MSFT':
                    new_stock = Stock(0, stock['Symbol'], 85, stock['Open'], stock['Close'], stock['Date'])
                    stock_dict[stock['Symbol']] = new_stock

                elif stock['Symbol'] == 'RDS-A':
                    new_stock = Stock(0, stock['Symbol'], 400, stock['Open'], stock['Close'], stock['Date'])
                    stock_dict[stock['Symbol']] = new_stock

            # Appending current prices to list
            stock_dict[stock['Symbol']].add_current_price(float(stock['Close']))

    # Prints if file doesn't exist
    except FileNotFoundError:
        print(json_file + " doesn't exist.")

    # Getting graph ready for input
    line_chart = pygal.Line(x_label_rotation=50, show_minor_x_labels=False)
    line_chart.title = 'Stock Values Over Time'

    # Sorting the dates by ascending order
    dates.sort(key=lambda date: datetime.strptime(date, "%d-%b-%y"))
    # Plotting every 50th date for readability
    line_chart.x_labels = map(str, dates)
    N = 50
    line_chart.x_labels_major = dates[::N]
    line_chart.value_formatter = lambda y: "${:,}".format(y)

    # Looping through dictionary and populating the graph
    for stock in stock_dict:
        prices = stock_dict[stock].current_value()
        while len(prices) < len(dates):
            prices.insert(0, None)
        line_chart.add(stock_dict[stock].stock_symbol, prices, dots_size=.1)

    # Exporting graph to file
    line_chart.render_to_file('line_chart.svg')

    # Setting db connection pointer
    db_connection = sqlite3.connect('test_db.db')
    cursor = db_connection.cursor()

    # SQL statements to make table and select from it
    sql_create_json_stock_table = """ CREATE TABLE IF NOT EXISTS json_stocks (
                                      stock_id integer,
                                      stock_symbol text, 
                                      total_shares,
                                      purchase_price real, 
                                      current_price real,
                                      current_value real, 
                                      purchase_date text);"""

    sql_select_json = """SELECT * FROM json_stocks;"""

    # Creating JSON table
    cursor.execute(sql_create_json_stock_table)

    for stock in stock_dict:
        current_values = stock_dict[stock].current_value()
        for value in current_values:
            cursor.execute("""INSERT OR REPLACE INTO json_stocks (stock_id, stock_symbol, total_shares, purchase_price,
                                               current_price, current_value, purchase_date) 
                                               VALUES (?,?,?,?,?,?,?)""", (stock_dict[stock].get_stock_id(),
                                                                           stock_dict[stock].stock_symbol,
                                                                           stock_dict[stock].total_shares,
                                                                           stock_dict[stock].purchase_price,
                                                                           stock_dict[stock].current_price,
                                                                           value,
                                                                           stock_dict[stock].purchase_date,))

    # Committing db changes
    db_connection.commit()

    # Printing data from db to check it
    # Uncomment to check
    # for stock in cursor.execute(sql_select_json):
        # print(stock[0], stock[1], stock[5], stock[6])

    # Closing the db connection
    db_connection.close()

    # Letting user know a pygal chart can be viewed in folder
    print('An pygal graph named "line_chart.svg" is ready for viewing.')
    print('It is located in the project folder.\n')

