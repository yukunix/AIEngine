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
    next(file)
    for line in file:
        close_index = line[4]
        all_close_index.append(float(close_index))
    all_close_index.reverse()
    
def rate_of_return(early_index, now_index):
    return (now_index - early_index) / early_index

# return a list of all daily rate of returns based on the time interval from 2007 - 2017.
def all_returns(data, period):
    my_return = []
    start = 0
    end = period
    print(int(len(data)/period))
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
    max_return = []
    start = 0
    end = period
    for i in range(0, int(len(data)/period)):
        period_index = data[start: end + 1]   ### calculation of LAST date in a period
        for j in range(0, period):             ## needs the FIRST daily index in the next
            if j+1 >= len(period_index):
                break
            profit = []                         # period.
            profit.append(rate_of_return(period_index[j], period_index[j + 1]))
            max_return.append(max(profit))
        start += period
        end += period
    return max_return

# test: - output the rate of return of first 5 time intervals since 2007/4/2.
#       - output the the first 5 max daily rate of return in each time interval.
print(all_returns(all_close_index, time_interval)[0:5])
print(find_max(all_close_index, time_interval)[0:5])
