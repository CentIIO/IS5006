# ALL IMPORTS NEEDED FOR THIS CLASS 
import random
from collections import defaultdict
from threading import Lock
import logging
from constants import seed
import json

random.seed(seed)

# CLASS GOOGLEADS
class GoogleAds(object):
    # THE DIFFERENT TYPES OF ADVERTS AVAILABLE
    ADVERT_BASIC = 'BASIC'
    ADVERT_TARGETED = 'TARGETED'
    ADVERT_BUNDLED = 'BUNDLED'

    #DICTIONARY WITH KEY AS ADVERT TYPE AND VALUE AS PRICE OF THE PARTICULAR ADVERT TYPE
    advert_price = {
        ADVERT_BASIC: 5,
        ADVERT_TARGETED: 10
    }

    #GOOGLE'S INTERNAL DATABASE COMPRISING OF A LIST TO STORE USERS, AND TWO DICTIONARIES TO STORE EXPENSES AND 
    #TRACK USER PURCHASE HISTORY RESPECTIVELY
    users = []
    expenses = defaultdict(list)
    purchase_history = defaultdict(list)

    lock = Lock()

    # FUNCTION TO POST ADVERTISEMENT FOR A PRODUCT PERTAINING TO A SELLER BASED ON AD_TYPE AND SCALE SET
    @staticmethod
    def post_advertisement(seller, product, advert_type, scale):
        
        # SCALE OF ADVERTS SHOULD NOT BE MORE THAN NUMBER OF USERS
        scale = min(scale, len(GoogleAds.users))
        GoogleAds.lock.acquire()

        # CHECK FOR ADVERT TYPE AND IF ADVERT_TYPE IS THEN CHOOSE ANY SET OF CUSTOMERS
        if advert_type == GoogleAds.ADVERT_BASIC:
            users = random.choices(GoogleAds.users, k=scale)
            test = ', '.join(x.name for x in users)
            logging.info('[GoogleAds]: Google pushed the %s Ad for product %s to users %s ', advert_type, product.name,
                         test)
            
        # CHECK IF ADVERT_TYPE IS TARGETED, THEN CHOOSE USERS WHO DON’T OWN THE PARTICULAR PRODUCT 
        elif advert_type == GoogleAds.ADVERT_TARGETED:
            new_users = list(set(GoogleAds.users) - set(GoogleAds.purchase_history[product]))
            users = random.choices(new_users, k=scale)
            test = ', '.join(x.name for x in users)
            logging.info('[GoogleAds]: Google pushed the %s Ad for product %s to user %s ', advert_type, product.name,
                         test)
        else:
            print('Not a valid Advert type')
            GoogleAds.lock.release()
            return

        # PUBLISH THE ADVERT TO SELECTED USERS
        scale = len(users)
        for user in users:
            user.view_advert(product)

        # UPDATE THE BILL INTO SELLER'S ACCOUNT AND ADD TO THE EXPENSE DICTIONARY
        bill = scale * GoogleAds.advert_price[advert_type]
        GoogleAds.expenses[seller.name].append(bill)
        data = json.loads(json.dumps(GoogleAds.expenses))
        logging.info('[GoogleAds]: Google billed the Seller %s  ', data)
        GoogleAds.lock.release()

        # RETURN THE BILL AMOUNT TO THE SELLER
        return bill

    # FUNCTION TO REGISTER USERS TO THE LIST OF USERS MAINTAINED BY GOOGLE
    @staticmethod
    def register_user(user):
        GoogleAds.lock.acquire()
        GoogleAds.users.append(user)
        logging.info(
            "[GoogleAds]:Customer %s added to Google list of user with quality/price/sentiment Tolerance:%s,%s,%s",
            user.name, user.quality_tolerance, user.price_tolerance, user.sentiment_tolerance)
        GoogleAds.lock.release()

    # FUNCTION TO TRACK USER PURCHASE HISTORY
    @staticmethod
    def track_user_purchase(user, product):
        GoogleAds.lock.acquire()
        GoogleAds.purchase_history[product.name].append(user.name)
        for i in GoogleAds.purchase_history.items():
            s = str(i)
            if not (s.startswith("(<p")):
                logging.info('[GoogleAds]: Google purchase history %s ', s)
        GoogleAds.lock.release()

    # FUNCTION TO COMPUTE USER COVERAGE
    @staticmethod
    def user_coverage(product):
        return len(set(GoogleAds.purchase_history[product])) / len(GoogleAds.users)
