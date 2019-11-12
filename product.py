import logging

class Product(object):
    
    def __init__(self, name, price, quality, release_date = 0, initial_amount= 100, reproduce_period = 999, reproduce_amount = 0):
        assert quality <= 1

        self.name = name
        self.price = price
        self.quality = quality
        self.accessories = []
        self.release_date = release_date
        self.initial_amount = initial_amount
        self.reproduce_period = reproduce_period
        self.reproduce_amount = reproduce_amount
        logging.info ("[Product]:Product created::%s ",self.name)

    def update_price(self, new_price):
        self.price = new_price

    def add_accessory(self, products):
        for product in products:
            if product not in self.accessories:
                self.accessories.append(product)