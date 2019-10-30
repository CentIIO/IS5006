from collections import defaultdict
import logging

class Twitter(object):
    # dictionary to store tweets
    feed = defaultdict(list)
    feed1 = defaultdict(list)
    # Called by the user to tweet something
    @staticmethod
    def post(user, product, tweet):
        Twitter.feed[product.name].append((user.name, tweet))
        #Twitter.feed1[product.name].append((user.name, tweet))
        for i in Twitter.feed.items():
            s=str(i)
            if not (s.startswith("(<p")):
                logging.info ('[Twitter]:History of Twitter post %s ',s)
    # returns the latest tweet about a product.
    @staticmethod
    def get_latest_tweets(product, n):
        return [tweet for user, tweet in Twitter.feed[product][-n:]]
