import logging

# PRODUCT CLASS
class Product(object):

    # INITIALIZATION OF EACH PRODUCT WITH DEFAULT VALUES IN CASE VALUES NOT FOUND IN CSV
    def __init__(self, name, price, quality, launchtick = 0, quantity= 100):
        assert quality <= 1
        self.name = name
        self.price = price
        self.quality = quality
        self.accessories = []
        self.launchtick = launchtick
        self.quantity = quantity
        logging.info ("[Product]:Product created::%s ",self.name)

    # UPDATE PRICE METHOD THAT UPDATES THE PRICE OF THE PRODUCT WITH PRICE PASSED.
    def update_price(self, new_price):
        self.price = new_price

    # ADD ACCESSORY OF A PARTICULAR PRODUCT WITH THE MAIN PRODUCT FOR THE PURPOSE OF BUNDLING
    def add_accessory(self, products):
        for product in products:
            if product not in self.accessories:
                self.accessories.append(product)