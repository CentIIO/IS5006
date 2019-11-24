# add product accessory support
from threading import Lock
from google_ads import GoogleAds
import logging
from tinydb import TinyDB as db
from tinydb import TinyDB as dbquery

class Market(object):
    catalogue = {}
    inventory = {}
    lock = Lock()

    # initialise the seller catalogue
    @staticmethod
    def register_seller(seller, product):
        Market.lock.acquire()
        logging.info("[Market]:Seller %s is registered in the market with the product %s ",seller.name,product.name)
        Market.catalogue[product] = seller
        # print("[market] register product:{}".format(product.name))
        Market.inventory[product] = 0
        Market.lock.release()

    # when a user buys a product, increment the seller's sales
    @staticmethod
    def buy(buyer, product):
        # get the seller for product from catalogue
        seller = Market.catalogue[product]

        # call seller's sold function
        seller.sold(product)
        logging.info("[Market]:Notify Seller %s about the sale of product %s ",seller.name,product.name)
        # deduct price from user's balance
        buyer.deduct(product.price)
        logging.info("[Market]:Get the amount $ %s from buyer %s for product %s ",product.price,buyer.name,product.name)
        Market.inventory[product] -= 1
        # track user
        GoogleAds.track_user_purchase(buyer, product)
        logging.info("[Market]:Add buyer %s purchased the product %s to google Add track history",buyer.name,product.name)

    @staticmethod
    def update_inventory(product, amount):
        Market.lock.acquire()
        Market.inventory[product] += amount
        Market.lock.release()

    @staticmethod
    def get_inventory(product):
        return Market.inventory[product]
