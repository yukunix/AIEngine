# coding = utf-8
"""author = jingyuan zhang"""
from config import Config
import tensorflow as tf
import os
import random
import numpy as np
from stock_scraper import StockScraper
from data_util import DataUtil
from config import ASingleStockConfig
import time
import sys
from copy import copy


class Reinforcer:
    def __init__(self):
        self.config = Config()
        self.du = DataUtil(self.config)
        self.sc = StockScraper(ASingleStockConfig())
        self.actions = [5000, 1000, 0, -1000, -5000]
        self.config.ACTION_NUM = len(self.actions)
        self.memories = []
        self.W1 = tf.get_variable('W1', [self.config.INPUT, self.config.M1])
        self.b1 = tf.get_variable('b1', [self.config.M1])
        self.W2 = tf.get_variable('W2', [self.config.M1, self.config.M2])
        self.b2 = tf.get_variable('b2', [self.config.M2])
        self.W3 = tf.get_variable('W3', [self.config.M2, 1])
        self.b3 = tf.get_variable('b3', [1])


        self.current_data = []
        self.current_state = []

        self.portfolio = {'fund':500000, 'stock_quantity':10000, 'current_stock_price':0, 'total': -1, 'stock_value':0}

        # self.init_op = tf.initialize_all_variables()
        self.init_placeholder()
        scores = self.batch_scoring_op()
        next_step_scores = self.batch_predict_op()
        self.add_loss_n_train_op(scores, next_step_scores)
        self.add_step_predict_op()
        self.saver = tf.train.Saver()

        self.init_op = tf.initialize_all_variables()

    def init_placeholder(self):
        self.states = tf.placeholder(tf.float32)
        self.rewards = tf.placeholder(tf.float32)
        self.states_next = tf.placeholder(tf.float32)

    def batch_scoring_op(self):
        x = tf.reshape(self.states, (self.config.BATCH_SIZE, self.config.INPUT))
        scores = self.Q_network_op(x)
        return scores

    def add_loss_n_train_op(self, scores, next_scores):
        self.predict_scores = self.config.gamma * tf.reduce_max(next_scores, 1)
        self.viewing_scores = scores
        '''sarsa reward better?'''
        self.losses = (self.rewards + self.predict_scores - scores) ** 2
        self.loss = tf.reduce_sum(self.losses)
        optimizer = tf.train.RMSPropOptimizer(self.config.lr)
        self.train_op = optimizer.minimize(self.loss)

    def add_step_predict_op(self):
        x = tf.reshape(self.states, (self.config.ACTION_NUM, self.config.INPUT))
        scores = self.Q_network_op(x)
        self.prediction = tf.argmax(tf.reshape(scores, (-1, self.config.ACTION_NUM)), axis=1)[0]

    def Q_network_op(self, x):
        fc1 = tf.matmul(x, self.W1) + self.b1
        relu1 = tf.nn.tanh(fc1)
        relu1 = tf.nn.dropout(relu1, self.config.DROPOUT)
        fc2 = tf.matmul(relu1, self.W2) + self.b2
        relu2 = tf.nn.tanh(fc2)
        relu2 = tf.nn.dropout(relu2, self.config.DROPOUT)
        scores = tf.matmul(relu2, self.W3) + self.b3
        scores = tf.squeeze(scores)
        return scores

    def batch_predict_op(self):
        x = tf.reshape(self.states_next, (self.config.BATCH_SIZE * self.config.ACTION_NUM, self.config.INPUT))
        Q_scores = self.Q_network_op(x)
        Q_scores = tf.reshape(Q_scores, (self.config.BATCH_SIZE, self.config.ACTION_NUM))
        return Q_scores

    def build_feed_dict(self, random_memories):
        feed = {}
        feed[self.states] = [m[0] for m in random_memories]
        states_next = []
        feed[self.rewards] = [m[1] for m in random_memories]
        new_portfolios = [m[-1] for m in random_memories]
        new_datas = [m[-2] for m in random_memories]
        assert len(new_datas) == len(new_portfolios)
        for i in range(len(new_datas)):
            port = new_portfolios[i]
            data = new_datas[i]
            for action in self.actions:
                action = self.action_policy(action, port)
                port_to_be_evaluated = self.update_portfolio_after_action(port, action)
                state_to_be_evaluated = self.du.preprocess_state(data, port_to_be_evaluated)
                states_next.append(state_to_be_evaluated)
        feed[self.states_next] = states_next
        return feed

    def action_policy(self, buy_quantity, portfolio):
        stock_price = portfolio['current_stock_price']
        fund = portfolio['fund']
        stock_quantity = portfolio['stock_quantity']
        if buy_quantity > 0:
            if buy_quantity * stock_price > fund:
                quantity_max = fund / stock_price
                for action in self.actions[::-1]:
                    if action <= quantity_max:
                        buy_quantity = action
            return buy_quantity
        elif buy_quantity < 0:
            if buy_quantity > stock_quantity:
                for action in self.actions:
                    if -action < stock_quantity:
                        buy_quantity = action
            return buy_quantity
        else:
            return 0

    @staticmethod
    def update_portfolio_after_action(portfolio, action):
        print 'action', action
        port = copy(portfolio)
        if action == 0:
            return port
        else:
            print 'a', port['fund'], 'b', port['current_stock_price'], 'c',action
            port['fund'] = port['fund'] - port['current_stock_price'] * action
            port['stock_quantity'] += action
            port['stock_value'] += port['current_stock_price'] * action
            return port
    @staticmethod
    def update_portfolio_after_fetch_price(portfolio, new_price):
        port = copy(portfolio)
        port['current_stock_price'] = new_price
        port['stock_value'] = new_price * port['stock_quantity']
        port['total'] = port['stock_value'] + port['fund']
        return port

    @staticmethod
    def calc_reward(new_portfolio, prev_portfolio):
        return 100.0*(new_portfolio['total'] - prev_portfolio['total']) / prev_portfolio['total']

    def run_epoch(self, session, save=None, load=None):
        if not os.path.exists('./save'):
            os.makedirs('./save')
        if load:
            self.saver.restore(session, load)
        else:
            session.run(self.init_op)

        while True:
            if self.portfolio['total'] == -1:
                init_data = self.sc.request_api()
                print init_data
                if init_data[self.config.open_price_ind]:
                    # assert init_data[self.config.open_price_ind] == init_data[self.config.current_ind]
                    self.portfolio['current_stock_price'] = init_data[self.config.current_ind]
                    self.portfolio['stock_value'] = self.portfolio['stock_quantity'] * self.portfolio['current_stock_price']
                    self.portfolio['total'] = self.portfolio['stock_value'] + self.portfolio['fund']
                    self.current_data = init_data
                    self.current_state = self.du.preprocess_state(init_data, self.portfolio)
                    self.config.INPUT = len(self.current_state)
                else:
                    print "market closed or stock halts"
                    sys.exit(0)
                print self.config.INPUT
            is_exploration = random.random()
            assert self.portfolio['current_stock_price'] != 0
            if is_exploration <= self.config.EPSILON:
                buy_quantity = random.choice(self.actions)

            else:
                candidates = []

                for action in self.actions:
                    action = self.action_policy(action, self.portfolio)
                    candidate_portfolio = self.update_portfolio_after_action(self.portfolio, action)
                    candidate_state = self.du.preprocess_state(self.current_data, candidate_portfolio)
                    candidates.append(candidate_state)
                max_q_ind = sess.run(self.prediction, feed_dict={self.states: candidates})
                buy_quantity = self.actions[max_q_ind]

            '''fetch!!!'''
            time.sleep(self.sc.config.time_interval)
            new_data = self.sc.request_api()
            '''update my portfolio & get reward'''
            new_portfolio = self.update_portfolio_after_action(self.portfolio, buy_quantity)
            assert (new_portfolio['current_stock_price'] * new_portfolio['stock_quantity'] + new_portfolio['fund']) == new_portfolio['total']
            self.portfolio = new_portfolio
            self.current_state = self.du.preprocess_state(self.current_data, self.portfolio)
            new_price = new_data[self.config.current_ind]
            new_portfolio = self.update_portfolio_after_fetch_price(new_portfolio, new_price)
            assert (new_portfolio['current_stock_price'] * new_portfolio['stock_quantity'] + new_portfolio['fund']) == new_portfolio['total']

            reward = self.calc_reward(new_portfolio, self.portfolio)


            '''now current state is a state where price is old while action has been performed'''
            '''new_state is a state where price is new and with new portfolio, but has not made furthur action yet'''
            self.memories.append((self.current_state, reward, new_data, new_portfolio))

            '''update data and portfolio'''
            self.current_data = new_data
            self.portfolio = new_portfolio

            if len(self.memories) > 10*self.config.BATCH_SIZE:
                start_ind = random.randint(0,len(self.memories)-self.config.BATCH_SIZE)
                batch = self.memories[start_ind:start_ind+self.config.BATCH_SIZE]
                '''batch BS*I'''
                feed = self.build_feed_dict(batch)
                scores1, scores2, losses, loss, _ = sess.run([self.predict_scores, self.viewing_scores, self.losses, self.loss, self.train_op], feed_dict=feed)
                print loss

if __name__ == '__main__':
    cc = Reinforcer()
    with tf.Session() as sess:
        cc.run_epoch(sess)






