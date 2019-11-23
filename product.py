import logging

class Product(object):
    
    def __init__(self, name, price, quality, launchtick = 0, quantity= 100):
        assert quality <= 1

        self.name = name
        self.price = price
        self.quality = quality # the qulaity has to
        self.accessories = []
        self.launchtick = launchtick
        self.quantity = quantity
        # self.reproduce_period = reproduce_period #what is the purpose of this?
        # self.reproduce_amount = reproduce_amount  #what is the purpose of this?
        logging.info ("[Product]:Product created::%s ",self.name)

    def update_price(self, new_price):
        self.price = new_price

    #its more like existing as a seperate product and linking how two similar products are related
    def add_accessory(self, products):
        for product in products:
            if product not in self.accessories:
                self.accessories.append(product)