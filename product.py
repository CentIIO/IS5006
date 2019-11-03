import logging

class Product(object):
    
    def __init__(self, name, price, quality):
        assert quality <= 1

        self.name = name
        self.price = price
        self.quality = quality
        logging.info ("[Product]:Product created::%s ",self.name)

    def update_price(self, new_price):
        self.price = new_price
