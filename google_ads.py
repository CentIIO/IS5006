import random
from collections import defaultdict
from threading import Lock
import logging
from constants import seed
import json
random.seed(seed)


class GoogleAds(object):
    # Define the types of adverts available
    ADVERT_BASIC = 'BASIC'
    ADVERT_TARGETED = 'TARGETED'
    ADVERT_BUNDLED='BUNDLED'

    # Define advert's price
    advert_price = {
        ADVERT_BASIC: 5,
        ADVERT_TARGETED: 10,
        ADVERT_BUNDLED:7
    }

    # Google's internal database
    users = []
    expenses = defaultdict(list)
    purchase_history = defaultdict(list)

    lock = Lock()

    # post an advert about the product
    @staticmethod
    def post_advertisement(seller, product, advert_type, scale):
        # scale of adverts should not be more than number of users
        scale = min(scale, len(GoogleAds.users))
        GoogleAds.lock.acquire()
        
        # if advert_type is basic, choose any set of customers
        if advert_type == GoogleAds.ADVERT_BASIC:
            users = random.choices(GoogleAds.users, k=scale)
            test=', '.join(x.name for x in users)
            logging.info ('[GoogleAds]: Google pushed the %s Ad for product %s to users %s ',advert_type,product.name,test)
        # if advert_type is targeted, choose user's who were not shown the same advert in previous tick
        elif advert_type == GoogleAds.ADVERT_TARGETED:
            new_users = list(set(GoogleAds.users) - set(GoogleAds.purchase_history[product]))
            users = random.choices(new_users, k=scale)
            test=', '.join(x.name for x in users)
            logging.info ('[GoogleAds]: Google pushed the %s Ad for product %s to user %s ',advert_type,product.name,test)
        else:
            print('Not a valid Advert type')
            return

        # publish the advert to selected user
        scale = len(users)
        for user in users:
            user.view_advert(product)

        # update the bill into seller's account
        bill = scale * GoogleAds.advert_price[advert_type]
        GoogleAds.expenses[seller.name].append(bill)
        data=json.loads(json.dumps(GoogleAds.expenses))
        logging.info ('[GoogleAds]: Google billed the Seller %s  ',data)
        GoogleAds.lock.release()

        # return the bill amount to the seller
        return bill

    @staticmethod
    def register_user(user):
        GoogleAds.lock.acquire()
        GoogleAds.users.append(user)
        logging.info("[GoogleAds]:Customer %s added to Google list of user with quality/price/sentiment Tolerance:%s,%s,%s",user.name,user.quality_tolerance,user.price_tolerance,user.sentiment_tolerance)
        GoogleAds.lock.release()

    @staticmethod
    def track_user_purchase(user, product):
        GoogleAds.lock.acquire()
        GoogleAds.purchase_history[product.name].append(user.name)
        for i in GoogleAds.purchase_history.items():
            s=str(i)
            if not (s.startswith("(<p")):
                logging.info ('[GoogleAds]: Google purchase history %s ',s)
        GoogleAds.lock.release()

    @staticmethod
    def user_coverage(product):
        return len(set(GoogleAds.purchase_history[product])) / len(GoogleAds.users)
