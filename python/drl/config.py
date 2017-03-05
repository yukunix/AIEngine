# coding = utf-8
"""author = jingyuan zhang"""


class Config:
    def __init__(self):
        self.BATCH_SIZE = 32
        self.UNCHANGED_TOLERENCE = 10
        self.EPSILON = 0.1
        self.MAXSTEP = 100
        self.MAXTIMESTEP = 200
        self.START_TIMESTEP = 50
        self.INPUT = 21
        self.ACTION_NUM = 5
        self.M1 = 20
        self.M2 = 5
        self.lr = 1e-6
        self.gamma = 0.015
        self.STOCK_AMOUNT = 16
        # self.TRANSACTION_AMOUNT = 100
        self.BENCHMARK_RETURN_INDEX = 14
        self.DROPOUT = 0.5
        self.INTERVAL = 5
        self.open_price_ind = 0
        self.yesterday_closing_price_ind = 1
        self.current_ind = 2
        self.today_highest_ind = 3
        self.today_lowest_ind = 4
        self.highest_buy_bid_ind = 5
        self.highest_sell_bid_ind = 6
        self.trade_quantity_ind = 7
        self.prev_rate_ind = 8


class ASingleStockConfig:
    def __init__(self):
        self.BATCH_SIZE = 32
        self.DROPOUT = 0.5
        self.code = '601766'
        self.type = 'sh'
        self.time_interval = 2
        self.outfile = '601766_60.txt'
