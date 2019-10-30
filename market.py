from threading import Lock
from google_ads import GoogleAds
import logging

class Market(object):
    catalogue = {}
    lock = Lock()

    # initialise the seller catalogue
    @staticmethod
    def register_seller(seller, product):
        Market.lock.acquire()
        logging.info("[Market]:Seller %s is registered in the market with the product %s ",seller.name,product.name)
        Market.catalogue[product] = seller
        Market.lock.release()

    # when a user buys a product, increment the seller's sales
    @staticmethod
    def buy(buyer, product):
        # get the seller for product from catalogue
        seller = Market.catalogue[product]

        # call seller's sold function
        seller.sold()
        logging.info("[Market]:Notify Seller %s about the sale of product %s ",seller.name,product.name)
        # deduct price from user's balance
        buyer.deduct(product.price)
        logging.info("[Market]:Get the amount $ %s from buyer %s for product %s ",product.price,buyer.name,product.name)
        # track user
        GoogleAds.track_user_purchase(buyer, product)
        logging.info("[Market]:Add buyer %s purchased the product %s to google Add track history",buyer.name,product.name)