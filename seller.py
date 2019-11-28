# ALL IMPORTS REQUIRED FOR THIS CLASS
import time
from threading import Lock, Thread
import numpy
import logging
from constants import tick_time
from google_ads import GoogleAds
from market import Market
from twitter import Twitter
import random
from rule_base_system import rbs_get_product_newamount, rbs_CEO_decide_new_price_budget
import Database as DB

# CLASS SELLER
class Seller(object):

    # INITIALIZATION OF SELLERS WITH THE CORRESPONDING ATTRIBUTES 
    def __init__(self, name, products, wallet):
        self.name = name
        self.products = []
        self.dbprod=[]
        self.dbacces=[]
        self.accessaries = []
        self.wallet = wallet
        logging.info("[Seller]:Seller %s Created", self.name)
        
        # DICTIONARIES TO STORE INFORMATION PERTAINING TO EACH SELLER SUCH AS -
        # TOTAL ITEMS SOLD, SALES HISTORY, EXPENSE HISTORY, SENTIMENT HISTORY, PRICE HOISTORY AND SO ON.
        self.item_sold = {}
        self.total_item_sold = {}
        self.sales_history = {}
        self.sentiment_history = {}
        self.expense_history = {}
        self.total_expense_history = [0]
        self.total_sales_history = []
        self.wallet_history = []
        self.inventory_history = {}
        self.price_history = {}
        self.adverts_type_history = {}
        self.adverts_scale_history = {}
        
        for product in products:
            
            # REGISTER THE SELLER IN MARKET
            if product not in self.products:
                self.products.append(product)
                
                # WRITING TO THE DB
                self.dbprod.append(product.name)
                Market.register_seller(self, product)
                
                # UPDATING INVENTORY WITH PRODUCT AMOUNT BASED ON LAUNCH TICK VALUE
                if product.launchtick == 0:
                    Market.update_inventory(product, product.quantity)
                    
                # INITAL VALUES ASSIGNED TO THE DICTIONARIES
                self.item_sold[product] = 0
                self.total_item_sold[product] = 0
                self.sales_history[product] = []
                self.sentiment_history[product] = []
                self.expense_history[product] = [0]
                self.inventory_history[product] = []
                self.price_history[product] = []
                self.adverts_type_history[product] = []
                self.adverts_scale_history[product] = []
                
                # ADDING THE ACCESSORY PRODUCT AND SAME OPERATION AS ABOVE
                for accessory in product.accessories:
                    if accessory not in self.products:
                        self.accessaries.append(accessory)
                        self.dbacces.append(accessory.name)
                        Market.register_seller(self, accessory)
                        if product.launchtick == 0:
                            Market.update_inventory(accessory, accessory.quantity)
                        self.item_sold[accessory] = 0
                        self.total_item_sold[accessory] = 0
                        self.sales_history[accessory] = []
                        self.sentiment_history[accessory] = []
                        self.expense_history[accessory] = [0]
                        self.inventory_history[accessory] = []
                        self.price_history[accessory] = []

        # METRICS TRACKING
        self.revenue_history = []
        self.profit_history = []
        self.month = []
        self.tickcount = 0
        
        # FLAG FOR THREAD
        self.STOP = False
        # UPDATING DB
        DB.update_SellerDB(self.name, str(self.dbprod), str(self.dbacces),(self.wallet))
        self.lock = Lock()

        # START THIS SELLLER IN SEPERATE THREAD
        self.thread = Thread(name=name, target=self.loop)
        self.thread.start()

    # LOOP 
    def loop(self):
        logging.info("[Seller]:Seller %s started Trading", self.name)
        while not self.STOP:
            self.tickcount += 1
            self.month.append(self.tickcount)
            logging.info("[Seller]:(%s,%d): Next month Begins ", self.name, self.tickcount)
            self.tick()
            time.sleep(tick_time)
        
        for product in self.products:
            logging.info("[Seller]: (%s,%d) sold  %d units of %s",
                         self.name, self.tickcount, self.total_item_sold[product], product.name)
        logging.info("[Seller]: (%s,%d) Exit", self.name, self.tickcount)

    # FUNCTION FOR PRODUCT SOLD
    def sold(self, product):
        self.lock.acquire()
        self.item_sold[product] += 1
        self.total_item_sold[product] += 1
        self.lock.release()

    # ONE TIMESTEP IN THE SIMULATION WORLD
    def tick(self):
        self.lock.acquire()
        for product in (self.products + self.accessaries):
            
            # APPEND THE SALES RECORD TO THE HISTORY
            self.sales_history[product].append(self.item_sold[product])
            
            # RESET THE SALESHISTORY COUNTER
            self.item_sold[product] = 0

            # INITIAL RELEASE OF PRODUCT
            if self.tickcount == product.launchtick and product.launchtick != 0:
                Market.update_inventory(product, product.quantity)
           
        self.lock.release()

        # CALCULATE THE METRICS FOR PREVIOUS TICK AND ADD TO TRACKER
        self.revenue_history.append(sum([self.sales_history[x][-1] * x.price for x in (self.products + self.accessaries)]))
        self.profit_history.append(self.revenue_history[-1] - sum([self.expense_history[x][-1] for x in self.products]))
        sentiments = self.user_sentiment()
        for product in self.products:
            self.sentiment_history[product].append(sentiments[product])

        # ADD THE PROFIT TO SELLER'S WALLET
        self.wallet += self.my_profit(True)

        # ASK DECISION FROM CEO REGARDING ADVER TYPE AND ADVERT BUDGET PER PRODUCT
        # ***** THE AD BUDGET IS PER PRODUCT SO SCALES IS A DICTIONARY 
        adverts, scales = self.CEO()
        
        logging.info ('[Seller]: (%s,%d) Revenue in previous month:%d', self.name,self.tickcount,self.my_revenue(True))
        logging.info ('[Seller]: (%s,%d) Expenses in previous month:%d', self.name,self.tickcount,self.my_expenses(True))
        logging.info ('[Seller]: (%s,%d) Profit in previous month:%d', self.name,self.tickcount,self.my_profit(True))
        sentiments = self.user_sentiment()
        for product in self.products:
            logging.info ('[Seller]: (%s,%d) Sentiment for %s in previous month:%d', self.name,self.tickcount,product.name, sentiments[product])
        
        # PERFORM THE ACTIONS AND VIEW THE EXPENSES
        total_expense_history= 0
        for product in self.products:
            product_expense = GoogleAds.post_advertisement(self, product, adverts[product], int(scales[product]))
            self.expense_history[product].append(product_expense)
            total_expense_history += product_expense
            self.inventory_history[product].append(Market.get_inventory(product))
            self.price_history[product].append(product.price)
            self.adverts_type_history[product].append((adverts[product]))
            self.adverts_scale_history[product].append(scales[product])
        self.total_sales_history.append(sum([self.sales_history[x][-1] for x in self.products]))
        self.total_expense_history.append(total_expense_history)
        self.wallet_history.append(self.wallet)


    # CALCULATE THE TOTAL REVENUE. GIVES THE REVENUE IN LAST TICK IF LATEST_ONLY = TRUE
    def my_revenue(self, latest_only=False):
        revenue = self.revenue_history[-1] if latest_only else numpy.sum(self.revenue_history)
        return revenue

    # CALCULATE THE TOTAL EXPENSE. GIVES THE REVENUE IN LAST TICK IF LATEST_ONLY = TRUE
    def my_expenses(self, latest_only=False):
        bill = 0
        for product in self.products:
            bill += self.expense_history[product][-1] if latest_only else numpy.sum(self.expense_history[product])
        return bill

    # CALCULATE THE TOTAL PROFIT. GIVES THE REVENUE IN LAST TICK IF LATEST_ONLY = TRUE
    def my_profit(self, latest_only=False):
        profit = self.profit_history[-1] if latest_only else numpy.sum(self.profit_history)
        return profit

    # CALCULATES THE PRODUCT SENTIMENT FROM TWEETS.
    def user_sentiment(self):
        sentiments = {}
        for product in self.products:
            tweets = numpy.asarray(Twitter.get_latest_tweets(product.name, 100))
            sentiments[product] = 1 if len(tweets) == 0 else (tweets == 'POSITIVE').mean()
        return sentiments

    # TO STOP THE SELLER THREAD
    def kill(self):
        logging.info ('[Seller]: (%s,%d) thread killed', self.name,self.tickcount)
        self.STOP = True
        self.thread.join(timeout=0)

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

        newbudget_total = 0
        adverts = {}
        scales = {}
        for product in self.products:
            
            # GET NEW PRICE AND NEW AD BUDGET FOR EACH PRODUCT
            if(self.tickcount == 1 or self.tickcount == 2 ):
                newprice = product.price
                newbudget = self.wallet // 3
            elif self.tickcount % 3 == 0:
                newprice, newbudget = rbs_CEO_decide_new_price_budget(product, self.sales_history[product], self.profit_history, self.expense_history[product][-1])
            else:
                newprice, newbudget =product.price, self.expense_history[product][-1]

            product.update_price(newprice)
            newbudget_total += newbudget

            # GET AD TYPE FOR EACH PRODUCT
            if (GoogleAds.user_coverage(product.name) < 0.5):
                adverts[product] = GoogleAds.ADVERT_BASIC
            else:
                adverts[product] = GoogleAds.ADVERT_TARGETED

            scales[product] = int(newbudget // GoogleAds.advert_price[adverts[product]])
            logging.info('[Seller]: (%s,%d) CEO selected advert_type as %s for %s',
                         self.name, self.tickcount, adverts[product], product.name)

        # AVOID SPEND MORE MONEY THAN WALLET USE 40% OF THE WALLET AMOUNT
        if newbudget_total > self.wallet * 0.4:
            reduce_ratio = newbudget_total / (self.wallet * 0.4)
            for product in self.products:
                scales[product] = scales[product] // reduce_ratio

        # UPDATE INVENTORY AT THE END OF EACH TICK
        for product in self.products:
            amtinInv = Market.inventory[product]
            newamount = rbs_get_product_newamount(product, amtinInv)
            Market.update_inventory(product, newamount - amtinInv)

        return adverts, scales
