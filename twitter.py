# ALL IMPORTS REQUIRED BY THE CLASS  
from collections import defaultdict
import logging
from copy import copy

# TWITTER CLASS 
class Twitter(object):
    # DICTIONARIES TO STORE DATA
    feed = defaultdict(list)
    feed1 = defaultdict(list)
    
    # FUNCTION TO POST A TWEET. IT IS CALLED BY THE CUSTOMER WHEN HE DECIDES TO TWEET ABOUT ONE OF HIS OWNED PRODUCTS
    @staticmethod
    def post(user, product, tweet):
        Twitter.feed[product.name].append((user.name, tweet))
        #Twitter.feed1[product.name].append((user.name, tweet))
        
        # THIS IS TO AVOID RUNTIMEERROR: DICTIONARY CHANGED SIZE DURING ITERATION
        twitter_feed_items = copy(Twitter.feed) 
        for i in twitter_feed_items:
            s=str(i)
            if not (s.startswith("(<p")):
                logging.info ('[Twitter]:History of Twitter post %s ',s)
                
    # FUNCTION THAT RETURNS THE LATEST TWEET ABOUT A PRODUCT.
    @staticmethod
    def get_latest_tweets(product_name, n):
        return [tweet for user, tweet in Twitter.feed[product_name][-n:]]
