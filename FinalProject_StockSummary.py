"""
This program is a combination of several
projects I worked on during this quarter.
It takes csv, json, and data from yfinance and
creates various graphs and outputs according to
what the user wants to see.
------------------------------------------------------------
ICT-4730-1 Python Programming
Stock Summary
Abby Smith
8/21/2022
"""

# Importing necessary functions
from StockAndBondFunctions import *
from yfinance_stock_functions import *

answer = input('Would you like to see some stocks? y/n\n')

while answer == 'y' or answer == 'Y':
    print('')
    print('What would you like to see today?')
    user_input = input("Press 'c' to see csv stocks, 'j' to see json stocks, or 'y' to bring up the yfinance menu\n")

    if user_input == 'c' or user_input == 'C':
        print('')
        print_csv_stocks()

    elif user_input == 'j' or user_input == 'J':
        print('')
        print_json_stocks()

    elif user_input == 'y' or user_input == 'Y':
        print('')
        plot_graphs(user_input)

    else:
        print('That was an invalid choice, please pick from c, j, or y.\n')
        continue

    # If the user wants to see other stocks, the loop continues.
    # Otherwise it stops and program finishes
    print('')
    answer = input('Would you like to make another selection? y/n\n')
    if answer == 'y' or answer == 'Y':
        continue
    else:
        break



