import random
import time
from threading import Thread, Lock
import logging
import numpy

from constants import tick_time, seed
from google_ads import GoogleAds
from market import Market
from twitter import Twitter
from fuzzy_logic import fuzzy_get_customer_tolerance

random.seed(seed)


class Customer(object):
    def __init__(self, name, wallet, type):
        self.name, self.wallet, self.type = name, wallet, type
        self.quality_tolerance, self.price_tolerance, self.sentiment_tolerance = fuzzy_get_customer_tolerance(type)
        logging.info ("[Customer]:Customer %s Created",self.name)
        # Register the user with google ads
        GoogleAds.register_user(self)

        # ad space stores all the adverts consumed by this user
        self.ad_space = set()
        # stores all the bought products
        self.owned_products = set()

        # flag to stop thread
        self.STOP = False

        # regulate synchronisation
        self.lock = Lock()
        self.tickcount=0
        # start this user in separate thread
        self.thread = Thread(name=name, target=self.loop)
        self.thread.start()
       
        
        
    # View the advert to this consumer. The advert is appended to the ad_space
    def view_advert(self, product):
        self.lock.acquire()
        self.ad_space.add(product)
        self.lock.release()

    # Consumer decided to buy a 'product'.
    def buy(self, product):
        # if not enough money in wallet, don't proceed
        if self.wallet < product.price:
            return

        if Market.inventory[product] == 0:
            return

        if self.price_tolerance < product.price:
            return
        # purchase the product from market
        
        Market.buy(self, product)

        # add product to the owned products list
        self.owned_products.add(product)

    # money is deducted from user's wallet when purchase is completed
    def deduct(self, money):
        self.wallet -= money

    # User expresses his sentiment about the product on twitter
    def tweet(self, product, sentiment):
        Twitter.post(self, product, sentiment)

    # Loop function to keep the simulation going
    def loop(self):
        logging.info ("[Customer]:Customer %s entered Trading",self.name)
        while not self.STOP:
            self.tickcount+=1    
            logging.info ("[Customer]:(%s,%d): Next Quarter Begins ",self.name,self.tickcount)
            self.tick()
            #Customer.next_q=Customer.next_q+1
            time.sleep(tick_time)
        test=', '.join(x.name for x in self.owned_products)
        logging.info("[Customer]: (%s,%d) own the Products:[%s] with balance of $ %d",self.name,self.tickcount,test,self.wallet)
        logging.info("[Customer]: (%s,%d) Exit", self.name,self.tickcount)

    # one timestep in the simulation world
    def tick(self):
        test=', '.join(x.name for x in self.ad_space)
        logging.info("[Customer]:(%s,%d) currently seeing ads for the Products:[%s]",self.name,self.tickcount,test)
        self.lock.acquire()
        # user looks at all the adverts in his ad_space
        for product in self.ad_space:
            # user checks the reviews about the product on twitter
            #print("Products",product.name)
            tweets = numpy.asarray(Twitter.get_latest_tweets(product.name, 100))
            #sprint("[", self.name,"]:Products",product.name,"Tweets=",tweets)
            user_sentiment = 1 if len(tweets) == 0 else (tweets == 'POSITIVE').mean()

            # ANSWER d.
            # if sentiment is more than user's sentiment tolerance and user does not have the product, then he/she may buy it with 20% chance. If it already has the product, then chance of buying again is 1%
            if user_sentiment >= self.sentiment_tolerance:
                if(product not in self.owned_products and random.random() < 0.1):
                    logging.info("[Customer]:***(%s,%d)bought the new product:[%s]",self.name,self.tickcount,product.name)
                    self.buy(product)
                    # buy accessory
                    for accessory in product.accessories:
                        if random.random() < 0.9 and accessory not in self.owned_products:
                            self.buy(accessory)
                elif (product in self.owned_products and random.random() < 0.01):
                    logging.info("[Customer]:$$$(%s,%d)bought the same product again:[%s]",self.name,self.tickcount,product.name)
                    self.buy(product)
                    # buy accessory
                    for accessory in product.accessories:
                        if random.random() < 0.9 and accessory not in self.owned_products:
                            self.buy(accessory)

            else:
                logging.info("[Customer]:###(%s,%d)doesn't buy any products ",self.name,self.tickcount)
        # remove the adverts from ad_space
        self.ad_space = set()
        test=', '.join(x.name for x in self.ad_space)
        logging.info("[Customer]:(%s,%d) Ad Space cleared ",self.name,self.tickcount)
        # with some chance, the user may tweet about the product
        if random.random() < 0.5 and len(self.owned_products) > 0:
            # he may choose any random product
            product = random.choice(list(self.owned_products))
            # sentiment in positive if the quality is higher than the quality tolerance
            if self.quality_tolerance < product.quality:
                sentiment = 'POSITIVE' 
            else:
                sentiment='NEGATIVE'
            # tweet sent
            self.tweet(product, sentiment)
            logging.info("[Customer]:(%s,%d) Posted %s tweet for the product %s",self.name,self.tickcount,sentiment,product.name)
        self.lock.release()

    # set the flag to True and wait for thread to join
    def kill(self):
        logging.info('[Customer]: (%s,%d) thread killed', self.name, self.tickcount)
        self.STOP = True
        self.thread.join(timeout=0)

    def __str__(self):
        return self.name
        
    def log_roundstatus(self):
        pass
