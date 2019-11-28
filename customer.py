# ALL IMPORTS NEEDED TO RUN THE CODE IN THIS CLASS
import random
import time
from threading import Thread, Lock
import logging
import numpy as np
import sqlite3
from sqlite3 import Error
from constants import tick_time, seed
from google_ads import GoogleAds
from market import Market
from twitter import Twitter
from rule_base_system import rbs_get_customer_attributes
import Database as DB


random.seed(seed)

# CUSTOMER CLASS
class Customer(object):
    
    # INITIALIZATION OF CUSTOMERS WITH ATTRIBUTES DERIVED FROM A FUNCTION IN RULE BASED SYSTEM. THE ATTRIBUTES DEPEND UPON CUSTOMER TYPE
    def __init__(self, name, wallet, type):
        self.name, self.wallet, self.type = name, wallet, type
        self.quality_tolerance, self.price_tolerance, self.sentiment_tolerance, self.ratio = rbs_get_customer_attributes(type)
        
        # SALARY IS GENERATED BASED ON NATIONAL STATISTICS AS PROVIDEED BY MOM USING NORMAL DISTRIBUTION WITH MEAN 5596 AND S.D OF 1865
        self.salary = np.random.normal(loc=5596, scale=1865, size=None)
        logging.info ("[Customer]:Customer %s Created",self.name)
        # REGISTERING THE USER IN GOOGLE ADS
        GoogleAds.register_user(self)
        
        # UPDATING CUSTOMER INFO IN THE DB
        DB.update_CustDB(self.name,str(self.wallet),self.type)

        # AD SPACE STORES ALL THE ADVERTS CONSUMED BY THIS USER
        self.ad_space = set()
        # SET TO STORE ALL THE PRODUCTS BOUGHT BY THE CUSTOMER
        self.owned_products = set()

        # FLAG TO STOP THREAD
        self.STOP = False

        # REGULATE SYNCHRONISATION
        self.lock = Lock()
        self.tickcount=0
        
        # START THIS USER IN SEPARATE THREAD
        self.thread = Thread(name=name, target=self.loop)
        self.thread.start()


        
    # FUNCTION TOADD THE AD OF A PRODUCT TO THE CUSTOMER'S AD SPACE
    def view_advert(self, product):
        self.lock.acquire()
        self.ad_space.add(product)
        self.lock.release()

    # FUNCTION BUY CHECKS FOR CONDITIONS TO DECIDE WHETHER PURCHASE OF PRODUCT WILL BE MADE BY CUSTOMER OR NOT
    def buy(self, product, user_sentiment):
        
        # IF WALLET DOES NOT HAVE ENOUGH DO NOT PROCEED
        if self.wallet < product.price:
            logging.info("[Customer]:***(%s,%d)bought the new product:[%s] fail due to wallet", self.name, self.tickcount, product.name)
            return False
        # IF THE PRODUCT IS OUT OF STOCK AND INVENTORY IS EMPTY
        if Market.inventory[product] == 0:
            logging.info("[Customer]:(%s,%d)no saleshistory for the product:[%s] fail due to inventory", self.name, self.tickcount, product.name)
            return False
        
        # CHECKS FOR USER'S PRICE TOLERANCE TO THE CURRENT PRICE OF THE PRODUCT 
        if self.price_tolerance < product.price:
            logging.info("[Customer]:(%s,%d)no saleshistory for the product:[%s] fail due to price_tolerance", self.name, self.tickcount, product.name)
            return False

        # CHECKS FOR USER'S SENTIMENT WITH THE SENTIMENT TOLERANCE SET
        if user_sentiment < self.sentiment_tolerance:
            logging.info("[Customer]:(%s,%d)no saleshistory for the product:[%s] fail due to sentiment_tolerance", self.name,
                         self.tickcount, product.name)
            return False
                
        # IF ALL CONDITIONS ARE MET THEN THE BUY METHOD PRESENT IN MARKET CLASS IS INVOKED
        Market.buy(self, product)

        # ADD PRODUCT TO THE OWNED PRODUCTS LIST
        self.owned_products.add(product)
        return True

    # MONEY IS DEDUCTED FROM USER'S WALLET WHEN PURCHASE IS COMPLETED
    def deduct(self, money):
        self.wallet -= money

    # User expresses his sentiment about the product on twitter
    def tweet(self, product, sentiment):
        Twitter.post(self, product, sentiment)

    # LOOP FUNCTION TO KEEP THE SIMULATION GOING
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

    # ONE TIMESTEP IN THE SIMULATION WORLD
    def tick(self):

        #LOGGING PART
        test=', '.join(x.name for x in self.ad_space)
        logging.info("[Customer]:(%s,%d) currently seeing ads for the Products:[%s]",self.name,self.tickcount,test)

        # USER LOOKS AT ALL THE ADVERTS PRESENT IN HIS AD_SPACE
        ad_space = self.ad_space.copy()
        for product in ad_space:

            # TWEETS FOR THE PRODUCT ARE GATHERED

            tweets = np.asarray(Twitter.get_latest_tweets(product.name, 100))
            
            # USER SENTIMENT CALCULATIION 
            user_sentiment = 1 if len(tweets) == 0 else (tweets == 'POSITIVE').mean()

            # CHECK WHETHER USER ALREADY OWNS PRODUCT IF NOT THEN CALL BUY FUNCTION
            if product not in self.owned_products:
                buy_result = self.buy(product,user_sentiment)
                
            # IF USER ALREADY OWNS THE PARTICULAR THEN HE BUYS BASED ON CHANCE
            elif (product in self.owned_products and random.random() < 0.1):
                logging.info("[Customer]:$$$(%s,%d)bought the same product again:[%s]", self.name, self.tickcount,
                             product.name)
                buy_result = self.buy(product,user_sentiment)
            else:
                buy_result = False
                logging.info("[Customer]:###(%s,%d)doesn't buy any products ", self.name, self.tickcount)
            
            # IF THE USER BUYS THE MAIN PRODUCT THEN HE CAN PURCHASE ITS ASSOCIATED ACCESSORIES
            if buy_result == True:
                for accessory in product.accessories:
                    
                    # THERE IS A VERY CHANCE OF HIM/HER BUYING THE ACCESSORY
                    if product in self.owned_products and random.random() < 0.9 and accessory not in self.owned_products:
                        #We set the user sentiment as 1 for accessory always in order to drive the bundling.
                        self.buy(accessory,1)

        # REMOVE ALL THE ADVERTISEMENTS FROM THE AD_SPACE
        self.lock.acquire()
        self.ad_space = set()
        self.lock.release()
        test=', '.join(x.name for x in self.ad_space)
        logging.info("[Customer]:(%s,%d) Ad Space cleared ",self.name,self.tickcount)
        
        # THE USER REVIEW IS BASED ON CHANCE
        if random.random() < 0.8 and len(self.owned_products) > 0:
            
            # HE RANDOMLY CHOOSES A PRODUCT FROM HIS LIST OF OWNED PRODUCTS
            product = random.choice(list(self.owned_products))
            # POSITIVE TWEET GUVEN IF PRODUCT QUALITY MATCHES THE USER'S QUALITY TOLERANCE
            if self.quality_tolerance < product.quality:
                sentiment = 'POSITIVE' 
            else:
                sentiment='NEGATIVE'
            # TWEET ASSIGNED TO THE PARTICULAR PRODUCT
            self.tweet(product, sentiment)
            logging.info("[Customer]:(%s,%d) Posted %s tweet for the product %s",self.name,self.tickcount,sentiment,product.name)
        self.lock.acquire()
        self.wallet += self.salary * self.ratio
        self.lock.release()
        logging.info("[Customer]:(%s,%d) wallet updated to %f from salary", self.name, self.tickcount, self.wallet)


    # SET THE FLAG TO TRUE AND WAIT FOR THREAD TO JOIN
    def kill(self):
        logging.info('[Customer]: (%s,%d) thread killed', self.name, self.tickcount)
        self.STOP = True
        self.thread.join(timeout=0)

    def __str__(self):
        return self.name
        
    def log_roundstatus(self):
        pass
