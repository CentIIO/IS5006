from collections import defaultdict
import logging
from copy import copy

class Twitter(object):
    # dictionary to store tweets
    feed = defaultdict(list)
    feed1 = defaultdict(list)
    # Called by the user to tweet something
    @staticmethod
    def post(user, product, tweet):
        Twitter.feed[product.name].append((user.name, tweet))
        #Twitter.feed1[product.name].append((user.name, tweet))
        twitter_feed_items = copy(Twitter.feed) # this is to avoid RuntimeError: dictionary changed size during iteration
        for i in twitter_feed_items:
            s=str(i)
            if not (s.startswith("(<p")):
                logging.info ('[Twitter]:History of Twitter post %s ',s)
    # returns the latest tweet about a product.
    @staticmethod
    def get_latest_tweets(product_name, n):
        return [tweet for user, tweet in Twitter.feed[product_name][-n:]]
