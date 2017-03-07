#coding=utf-8
__author__ = 'zhangjingyuan'
import urllib
from termcolor import colored
import subprocess
import datetime
import numpy as np
import time
import pickle
from config import ASingleStockConfig
# url_base = 'http://hq.sinajs.cn/list='

class StockScraper:
    def __init__(self, config):
        self.date = datetime.date.today()
        self.config = config
        self.code = config.code
        self.url_base = 'http://hq.sinajs.cn/list='
        self.stock_type = config.type #'sh' or 'sz'
        self.url = self.url_base + self.stock_type + self.code
        self.open_price = 0
        self.yesterday_closing_price = 0

    def print_content(self, features):
        print "代码: "+str(self.code)
        print '开盘价: '+str(features[0])
        print '昨收: '+str(features[1])
        print '现价: '+str(features[2])
        print '最高: '+str(features[3])
        print '最低: '+str(features[4])
        print '买一价: '+str(features[5])
        print '卖一价: '+str(features[6])
        print '交易量: '+str(features[7])
        reward = features[-1]
        if reward > 0:
            print colored(('涨跌幅: '+str(reward)+'%'), 'red')
        elif reward == 0:
            print '涨跌幅: '+str(reward)+'%'
        else:
            print colored(('涨跌幅: '+str(reward)+'%'), 'green')
        print

    def request_api(self):
        raw_content = urllib.urlopen(self.url)
        content = (raw_content.read().split(','))
        features = self.parse_content(content)
        features += self.request_market_index(self.config.type)
        print features
        self.append_to_file(features)

        # self.print_content(features)
        # data = np.array(features)
        return features

    def request_market_index(self, stock_type):
        return self.request_api_on_stock('000001', 's_'+stock_type, True)

    def append_to_file(self, data):
        with open(self.config.outfile, 'a') as f:
            args = [str(x) for x in data]
            line = ' '.join(args)
            f.write(line+'\n')

    def request_api_on_stock(self, code, stock_type, is_index=False):
        url = self.url_base + stock_type + str(code)
        raw_content = urllib.urlopen(url)
        content = (raw_content.read().split(','))
        # print content
        # data = self.parse_content(content)
        if is_index:
            data = self.parse_content_on_index(content)
        else:
            data = self.parse_content(content)
        # data = np.array(data)
        return data

    def parse_content_on_index(self, content):
        data = [float(x)for x in content[1:-1]]
        data.append(float(content[-1][:-3]))
        return data

    def parse_content(self, content):
        open_price = float(content[1])
        yesterday_closing_price = float(content[2])
        current = float(content[3])
        today_highest = float(content[4])
        today_lowest = float(content[5])
        highest_buy_bid = float(content[6])
        highest_sell_bid = float(content[7])
        trade_quantity = float(content[9])
        try:
            rate = round(((current - open_price) / open_price) * 100, 2)
        except ZeroDivisionError:
            rate = 0
        try:
            prev_rate = round(((current - yesterday_closing_price) / yesterday_closing_price) * 100, 2)
        except:
            prev_rate = 0

        features = [open_price, yesterday_closing_price, current, today_highest, today_lowest, highest_buy_bid, highest_sell_bid, trade_quantity,
                    prev_rate, rate]

        return features


def main():
    print
    print '********************* BEGINNING *********************'
    print
    config = ASingleStockConfig()
    stock = StockScraper(config)
    stock.request_api()
    print '************************ END ***********************'


if __name__ == '__main__':
    main()