# Uses Yahoo Finance S&P 500 statistics 2007-2017, avalaible at
# https://finance.yahoo.com, stored in the file SP500_Data.csv,
# assumed to be stored in the working directory.
# Prompts the user for a time interval (in date format), in order to
# calculate the rate of return based on the period.
# Outputs - the rate of return
#         - plot the graph
#
# Written by Michael Li
# Latest update: Mar 31

import os
import sys
import csv
import numpy as np

# make sure the data file is stored in the working directory.
filename = "SP500_Data.csv"
if not os.path.exists(filename):
    print("There is no file named {} in the working directory, giving up...".format(filename))
    sys.exit()

# make sure the input time interval is a positive integer.
try:
    time_interval = int(input("Please enter a time interval (in days): "))
    if int(time_interval) < 1: 
        print("Sorry the time interval has to be a positive integer, giving up...")
    if not time_interval:
        raise ValueError
except ValueError:
    print("Incorrect input, giving up...")
    sys.exit()

# collect all daily close index
with open(filename) as csvfile:
    file = csv.reader(csvfile)
    all_close_index = [] # all daily close index
    all_trade_dates = [] # all trading dates
    next(file)
    for line in file:
        close_index = line[4]
        trade_date = line[0]
        all_close_index.append(float(close_index))
        all_trade_dates.append(trade_date)
    all_close_index.reverse()

def rate_of_return(early_index, now_index):
    return (now_index - early_index) / early_index

# return a list of all period rate of returns based on the time interval from 2007 - 2017.
def all_returns(data, period):
    my_return = []
    start = 0
    end = period
    for i in range(0, int(len(data)/period)):
        if end >= len(data):
            break
        period_return = rate_of_return(data[start], data[end])
        my_return.append(period_return)
        start += period
        end += period
    return my_return

# find the max rate of return during each time interval from 2007 - 2017.
def find_max(data, period):
    if period == 1:
        return all_returns(data, 1)
    else:
        daily_returns = all_returns(data, 1)
        max_returns = []
        i = 0
        while i + period <= len(daily_returns):
            max_return = max(daily_returns[i:i+period])
            max_returns.append(max_return)
            i += period
        return max_returns

# demo: - output the rate of return of first 5 time intervals since 2007/4/2.
#       - output the the first 5 max period rate of return in each time interval.
print()
print("The first {} days rate of return based on "
      "a period of {} days:\n".format(time_interval * 5, time_interval))
for i in range(0, 5):
      print(all_returns(all_close_index, time_interval)[i])

print()
print("The first {} max rate of return "
      "based on the period of {} days:\n".format(5, time_interval))
for i in range(0, 5):
      print(find_max(all_close_index, time_interval)[i])

# ask the user to input two specific dates splitted by "~"
def console_usr():
    while True:
        try:
            start_date, end_date = input("Please enter the period of data you\'re "
                                         "interested in (e.g. 2017-03-15~2017-03-30) "
                                         "FORMATE: YYYY-MM-DD, splitted by "'"~"'": ").split("~")
            break
        except (ValueError, NameError):
            print("\nWrong input, format example: 2017-03-15~2017-03-30, try again!")
    return start_date, end_date

# console main
print()
start_date, end_date = console_usr()

# get the index data in the range that the usr interested in, store it in a list called temp
all_close_index.reverse()
with open(filename) as csvfile:
    file = csv.reader(csvfile)
    temp = []
    temp_dates = []
    next(file)
    for line in file:
        dates = line[0]
        if dates == end_date:
            temp_start = int(file.line_num - 2)
        if dates == start_date:
            temp_end = int(file.line_num - 2)
    temp.extend(all_close_index[temp_start:temp_end + 1])
    temp_dates.extend(all_trade_dates[temp_start:temp_end + 1])
    trading_days = temp_end - temp_start + 1

temp_returns = all_returns(temp,1)
avg_return = np.mean(temp_returns)
temp_max = find_max(temp, trading_days - 1)[0]
max_date = temp_dates[temp_returns.index(temp_max)] # find the date of max_daily return
print()
print("The average daily returns over the {} trading days is".format(trading_days), avg_return)
print("The max daily return is on {} with {}".format(max_date, temp_max))
