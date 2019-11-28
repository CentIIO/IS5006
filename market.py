from threading import Lock
from google_ads import GoogleAds
import logging

# MARKET CLASS TO SIMULATE THE OPERATIONS OF THE MARKET
class Market(object):

    # CATALOGUE IS A DICTIONARY WITH THE KEY AS THE MAIN PRODUCT AND VALUE AS THE SELLER SELLING IT
    catalogue = {}
    # INVENTORY IS A DICTIONARY WITH THE KEY AS MAIN PRODUCT AND VALUE BEING THE AMOUNT OF PRODUCT
    inventory = {}
    lock = Lock()

    # INITIALIZING THE SELLER CATALOGUE BY REGISTERING THE SELLER IN THE CATALOGUE AND ASSIGNING THE INVENTORY WITH THE PRODUCT AMOUNT
    @staticmethod
    def register_seller(seller, product):
        Market.lock.acquire()
        logging.info("[Market]:Seller %s is registered in the market with the product %s ",seller.name,product.name)
        Market.catalogue[product] = seller
        # print("[market] register product:{}".format(product.name))
        Market.inventory[product] = 0
        Market.lock.release()

    # BUY METHOD
    @staticmethod
    def buy(buyer, product):
        # GET SELLER INFO FOR THE PARTICULAR PRODUCT USING THE CATALOGUE
        seller = Market.catalogue[product]

        # CALLING THE SOLD FUNCTION AT THE TIME OF PRODUCT SALE
        seller.sold(product)
        logging.info("[Market]:Notify Seller %s about the sale of product %s ",seller.name,product.name)

        # DEDUCTING THE PRICE OF THE PRODUCT BOUGHT FROM THE CUSTOMER'S WALLET
        buyer.deduct(product.price)
        logging.info("[Market]:Get the amount $ %s from buyer %s for product %s ",product.price,buyer.name,product.name)
        Market.inventory[product] -= 1

        # TRACKING USERS THAT BOUGHT PARTICULAR PRODUCTS
        GoogleAds.track_user_purchase(buyer, product)
        logging.info("[Market]:Add buyer %s purchased the product %s to google Add track history",buyer.name,product.name)


    # THE UPDATE INVENTORY FUNCTION THAT IS USED TO UPDATE THE AMOUNT OF PRODUCT PER MONTH
    @staticmethod
    def update_inventory(product, amount):
        Market.lock.acquire()
        Market.inventory[product] += amount
        Market.lock.release()

    # THE GET INVENTORY FUNCTION WHICH IS USED TO GET INFO ABOUT AMOUNT OF PRODUCT REMAINING
    @staticmethod
    def get_inventory(product):
        return Market.inventory[product]
