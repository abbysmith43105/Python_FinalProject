"""
This module contains all of the functions used
to graph the stock data. A function that converts
database data to class objects is included as well.
------------------------------------------------------------
ICT-4730-1 Python Programming
Yfinance Stock Functions
Abby Smith
8/21/2022
"""

import matplotlib.pyplot as plt
import mplfinance as mpf
import sqlite3
from datetime import date, timedelta
import yfinance as yf
import pandas as pd

def plot_graphs(answer):
    # Stock symbols needed for getting the current data
    stock_symbols = ['AIG', 'GOOGL', 'META', 'SHEL', 'F', 'M', 'IBM', 'MSFT']

    # If user says y, the loop will execute, otherwise nothing will happen
    answer = answer
    while answer == 'y' or answer == 'Y':

        print('')
        print('What graph would you like to see?')
        user_input = input("Press 'c' for today's stock values, 's' for the six month values, "
                           "or 't' for value trends.\n")

        if user_input == 'c' or user_input == 'C':
            try:
                # Sending control to the plot_todays_price function
                # Uses data from yfinance
                plot_todays_price(stock_symbols)
            except Exception as e:
                print(e)

        elif user_input == 's' or user_input == 'S':
            try:
                # Sending control to the plot_six_months function
                # Uses data from yfinance
                plot_six_months(stock_symbols)
            except Exception as e:
                print(e)

        elif user_input == 't' or user_input == 'T':
            answer = 'y'
            # Asking the user what stock trends they would like to see
            # Candlestick graphs show market movement over time
            while answer == 'y' or answer == 'Y':
                print('')
                print('What stock trend would you like to see?')
                user_stock = input('Valid options are: GOOGL, META, SHEL, F, M, AIG, IBM, MSFT\n')
                if user_stock.upper() in stock_symbols:
                    try:
                        plot_trends(user_stock)
                    except Exception as e:
                        print(e)
                else:
                    print('')
                    print('Please enter a valid option.')
                    continue

                print('')
                answer = input('Would you like to see trends for a different stock? y/n\n')
                if answer == 'y' or answer == 'Y':
                    continue
                else:
                    break
        else:
            print('')
            print('That was an invalid choice, please pick from c, s, or t.\n')
            continue

        # If the user wants to see more graphs, control will go back to
        # the top of the loop. Otherwise, the loop will stop
        # and the database functions will be called.
        print('')
        answer = input('Would you like to see another graph? y/n\n')
        if answer == 'y' or answer == 'Y':
            continue
        else:
            break

    # Calling functions to make a table from stock data
    make_stock_table(stock_symbols)

    # uncomment to test database
    # select_stock()

# Function that gets the current stock price and plots it on a bar graph
# for each stock in the list
def plot_todays_price(symbols):
    fig, ax = plt.subplots()
    today = date.today()
    ax.set_title('Stock Prices For: ' + str(today.strftime("%B %d, %Y")))
    plt.xlabel('Stock Value in USD')
    plt.ylabel('Stock Symbol')
    ax.invert_yaxis()
    plt.xlim(0, 500)
    # Adding x and y gridlines to increase readability
    plt.grid(visible=True, color='grey',
             linestyle='-.', linewidth=0.5,
             alpha=0.2)

    # Looping through stock list and inserting into graph
    for symbol in symbols:
        stock_symbol = symbol
        get_stock_info = yf.Ticker(stock_symbol)
        todays_data = pd.DataFrame(get_stock_info.history(period='1d'))
        # Plotting horizontal bar graph
        plt.barh(stock_symbol, todays_data['Close'])

    # Adding annotation to bars to show stock value
    for i in ax.patches:
        plt.text(i.get_width() + 0.2, i.get_y() + 0.5,
                 '$' + str(round((i.get_width()), 2)),
                 fontsize=8, fontweight='bold',
                 color='grey')

    plt.show()


def plot_six_months(symbols):
    # Setting up the visual aspects of graph
    today = date.today()
    six_months_ago = today - timedelta(days=180)
    plt.suptitle("Stock Values for: " + str(six_months_ago.strftime("%B %d, %Y")) + ' to '
                 + str(today.strftime("%B %d, %Y")))
    plt.ylabel('US Dollars')
    plt.xlabel('Months')
    plt.xticks(fontsize=8)

    # Adding x and y gridlines to increase readability
    plt.grid(visible=True, color='grey',
             linestyle='-.', linewidth=0.5,
             alpha=0.2)

    # Getting stock symbols from list
    for symbol in symbols:
        # Getting the last six months of stock info from y finance.
        get_stock_info = yf.Ticker(symbol)
        six_month_data = pd.DataFrame(get_stock_info.history(period='6mo'))
        plt.plot(six_month_data.index, six_month_data['Close'], label=symbol)

        # Legend is in the loop because we need the stock symbol for it
        plt.legend(prop={'size': 6}, bbox_to_anchor=(1.02, 1.0),
                   loc='upper left', borderaxespad=0)

    plt.show()


def plot_trends(stock):

    # Getting stock info for the stock of the users choice
    get_stock_info = yf.Ticker(stock.upper())
    # Extracting three month period from data
    three_month_data = pd.DataFrame(get_stock_info.history(period='3mo'))
    # We don't need the dividends, splits, or volume so we are dropping them
    three_month_data.drop(['Dividends', 'Stock Splits', 'Volume'], axis=1, inplace=True)
    # Plotting a candlestick graph along with the moving average for 3, 6, and 9 days
    mpf.plot(three_month_data, axtitle=(stock.upper()+' candlestick graph'), type='candle', mav=(3,6,9), volume=False,
             show_nontrading=True, style='yahoo')

# Function that creates a database table using a years
# worth of stock data. After researching what time frame
# is best for stock analysis, 1 year seemed to be the
# best one.
def make_stock_table(stock_symbols):

    conn = sqlite3.connect('yfinance_stocks.db')
    cursor = conn.cursor()

    # Dropping table so theres only a years worth of data in table
    sql_drop_table = """DROP TABLE IF EXISTS stock;"""

    cursor.execute(sql_drop_table)

    # Getting the timeframe ready
    for stock in stock_symbols:
        get_stock_info = yf.Ticker(stock)
        one_yr_data = pd.DataFrame(get_stock_info.history(period='1y'))
        # We don't need dividends or splits, they don't have data in them anyways
        one_yr_data.drop(['High', 'Low', 'Dividends', 'Stock Splits', 'Volume'], axis=1, inplace=True)
        # Adding a new column for stock symbol
        one_yr_data['Symbol'] = stock

        # Using pandas dataframe to sql function to insert frame into table
        one_yr_data.to_sql(name='stock', if_exists='append', index=True, index_label='Date', con=conn)

    conn.commit()
    conn.close()


# This functions purpose is to test the table that was just made
def select_stock():
    # SQL to select stock info
    sql_select_stocks = """select Date, Open, Close, Symbol from stock"""

    conn = sqlite3.connect('yfinance_stocks.db')
    for stock in conn.execute(sql_select_stocks):
        try:
            print(stock[0], stock[3], stock[1], stock[2])

        except Exception as e:
            print(e)

    conn.close()


