#Authors:Haroon Basheer, Jack


import time
from threading import Lock, Thread

import numpy
import logging
from constants import tick_time
from google_ads import GoogleAds
from market import Market
from twitter import Twitter
import random


class Seller(object):

    def __init__(self, name, products, wallet):
        self.name = name
        self.products = []
        self.wallet = wallet
        logging.info ("[Seller]:Seller %s Created",self.name)
        self.item_sold = {}
        self.total_item_sold = {}
        self.sales_history = {}
        self.sentiment_history = {}
        self.expense_history = {}
        self.inventory_history = {}
        for product in products:
            # register the seller in market
            if product not in self.products:
                self.products.append(product)
                Market.register_seller(self, product)
                if product.launchtick == 0:
                    Market.update_inventory(product, product.quantity)
                self.item_sold[product] = 0
                self.total_item_sold[product] = 0
                self.sales_history[product] = []
                self.sentiment_history[product] = []
                self.expense_history[product] = [0]
                self.inventory_history[product] = []
                # add accessory product
                for accessory in product.accessories:
                    if accessory not in self.products:
                        self.products.append(accessory)
                        Market.register_seller(self, accessory)
                        if product.launchtick == 0:
                            Market.update_inventory(accessory, accessory.quantity)
                        self.item_sold[accessory] = 0
                        self.total_item_sold[accessory] = 0
                        self.sales_history[accessory] = []
                        self.sentiment_history[accessory] = []
                        self.expense_history[accessory] = [0]
                        self.inventory_history[accessory] = []

        # metrics tracker
        self.revenue_history = []
        self.profit_history = []
        self.quarter = []
        self.tickcount=0
        # Flag for thread
        self.STOP = False

        self.lock = Lock()

        # start this seller in separate thread
        self.thread = Thread(name=name, target=self.loop)
        self.thread.start()

    def loop(self):
        logging.info ("[Seller]:Seller %s started Trading",self.name)
        while not self.STOP:
            self.tickcount+=1
            self.quarter.append(self.tickcount)
            logging.info ("[Seller]:(%s,%d): Next Quarter Begins ",self.name,self.tickcount)
            self.tick()
            time.sleep(tick_time)
        #test=', '.join(x.name for x in self.sales_history)
        for product in self.products:
            logging.info("[Seller]: (%s,%d) sold  %d units of %s",self.name,self.tickcount,self.total_item_sold[product],product.name)
        logging.info("[Seller]: (%s,%d) Exit", self.name,self.tickcount)
    # if an item is sold, add it to the database
    def sold(self,product):
        self.lock.acquire()
        self.item_sold[product] += 1
        self.total_item_sold[product] +=1
        self.lock.release()

    # one timestep in the simulation world
    def tick(self):
        self.lock.acquire()
        for product in self.products:
            # append the sales record to the history
            self.sales_history[product].append(self.item_sold[product])
            # reset the sales counter
            self.item_sold[product] = 0

            # initial release of product
            if self.tickcount == product.launchtick and product.launchtick != 0:
                Market.update_inventory(product,product.quantity)
            # reproduce of product
            # if self.tickcount % product.reproduce_period == 0:
            #     Market.update_inventory(product, product.reproduce_amount)

            try:
                self.inventory_history[product].append(Market.get_inventory(product))
            except:
                print("[seller]exception: product name:{}".format(product.name))
        self.lock.release()

        # Calculate the metrics for previous tick and add to tracker
        self.revenue_history.append(sum([self.sales_history[x][-1] * x.price for x in self.products]))
        self.profit_history.append(self.revenue_history[-1] - sum([self.expense_history[x][-1] for x in self.products]))
        sentiments = self.user_sentiment()
        for product in self.products:
            self.sentiment_history[product].append(sentiments[product])

        # add the profit to seller's wallet
        self.wallet += self.my_profit(True)

        # choose what to do for next timestep
        adverts, scale = self.CEO()

        # ANSWER a. print data to show progress
        #test=', '.join(for x in self.sentiment_history)
        
        logging.info ('[Seller]: (%s,%d) Revenue in previous quarter:%d', self.name,self.tickcount,self.my_revenue(True))
        logging.info ('[Seller]: (%s,%d) Expenses in previous quarter:%d', self.name,self.tickcount,self.my_expenses(True))
        logging.info ('[Seller]: (%s,%d) Profit in previous quarter:%d', self.name,self.tickcount,self.my_profit(True))
        sentiments = self.user_sentiment()
        for product in self.products:
            logging.info ('[Seller]: (%s,%d) Sentiment for %s in previous quarter:%d', self.name,self.tickcount,product.name, sentiments[product])
        #logging.info ('[Seller]: (%s,%d) Sales in previous quarter:%d', self.name,self.tickcount,self.sales_history(True))
        #logging.info ('[Seller]: (%s,%d)Strategy for next quarter \nAdvert Type: {}, scale: {}\n\n'.format(advert_type, scale))
        
        # perform the actions and view the expense
        for product in self.products:
            self.expense_history[product].append(GoogleAds.post_advertisement(self, product, adverts[product], scale))

    # calculates the total revenue. Gives the revenue in last tick if latest_only = True
    def my_revenue(self, latest_only=False):
        revenue = self.revenue_history[-1] if latest_only else numpy.sum(self.revenue_history)
        return revenue

    # calculates the total revenue. Gives the revenue in last tick if latest_only = True
    def my_expenses(self, latest_only=False):
        bill = 0
        for product in self.products:
            bill += self.expense_history[product][-1] if latest_only else numpy.sum(self.expense_history[product])
        return bill

    # calculates the total revenue. Gives the revenue in last tick if latest_only = True
    def my_profit(self, latest_only=False):
        profit = self.profit_history[-1] if latest_only else numpy.sum(self.profit_history)
        return profit

    # calculates the user sentiment from tweets.
    def user_sentiment(self):
        sentiments = {}
        for product in self.products:
            tweets = numpy.asarray(Twitter.get_latest_tweets(product.name, 100))
            sentiments[product] = 1 if len(tweets) == 0 else (tweets == 'POSITIVE').mean()
        return sentiments

    # to stop the seller thread
    def kill(self):
        logging.info ('[Seller]: (%s,%d) thread killed', self.name,self.tickcount)
        self.STOP = True
        self.thread.join()

    def __str__(self):
        return self.name

    # Cognition system that decides what to do next.
    def CEO(self):
        # WRITE YOUR INTELLIGENT CODE HERE
        # You can use following functions to make decision
        #   my_revenue
        #   my_expenses
        #   my_profit
        #   user_sentiment
        #
        # You need to return the type of advert you want to publish and at what scale
        # GoogleAds.advert_price[advert_type] gives you the rate of an advert

        # incorporate intelligent rule based systems here

        # adjust price based on latest sales
        for product in self.products:
            if self.sales_history[product][-1] == 0 and random.random() < 0.5:
                product.update_price(product.price * 0.9)
                logging.info('[Seller]: (%s,%d) CEO  the decreased the price for the product',self.name,
            self.tickcount)
            if self.sales_history[product][-1] >= 2 and random.random() < 0.5:
                product.update_price(product.price * 1.1)
                logging.info('[Seller]: (%s,%d) CEO increased the price for the product',self.name,
                     self.tickcount)

        adverts = {}
        for product in self.products:
            if (GoogleAds.user_coverage(product.name) < 0.5):
                advert_type = GoogleAds.ADVERT_BASIC
            else:
                advert_type=GoogleAds.ADVERT_TARGETED
            adverts[product] = advert_type
            # print("[Seller]: CEO decide advert type for {} is {}.".format(product.name, advert_type))
            logging.info('[Seller]: (%s,%d) CEO selected advert_type as %s for %s', self.name,
                     self.tickcount, advert_type, product.name)
        #HOW SCALE OPERATION IS CALCULATED?? CAN THIS BE INTELLIGENT
        scale = int(self.wallet // sum([GoogleAds.advert_price[v] for k,v in adverts.items()]) // 2) #not spending everything
        logging.info('[Seller]: (%s,%d) CEO selected advert scale %s', self.name, self.tickcount, scale)
        return adverts, scale
