#task for assignment:
'''draw the flowchart and export metrics to google sheets'''


#task for project
'''implement the cognitive engine/ceo'''


#reference: lecture#08
import logging
import random
import names
import time
import constants as para
from customer import Customer
from product import Product
from seller import Seller
from utils import plot
import os
from datetime import datetime
import sys

now = datetime.now()
dt_string = now.strftime("%H%M%S_%d_%m_%Y")
#print("date and time =", dt_string)


logging.basicConfig(filename='Logs/'+dt_string+'.log', level=logging.INFO)
random.seed(para.seed)
#'consumer_' + str(i)
# Create 500  Consumers objects and assign initial with tolerance and wallet 
customers = [Customer(name=names.get_full_name(), wallet=500,tolerance=0.5 + 0.4 * random.random() ) for i in range(1,(para.numberofcustomer+1))]


# Construct a product object with following attributes
iphone = Product(name='iphoneX', price=300, quality=0.9)
galaxy = Product(name='Note', price=200, quality=0.8)
sony = Product(name='Xperia', price=100, quality=0.6)

# Create a Seller object with product as one of the attributes
seller_apple = Seller(name='APPLE INC', product=iphone, wallet=1000)
seller_samsung = Seller(name='SAMSUNG MOBILES', product=galaxy, wallet=500)
seller_sony = Seller(name='SONY', product=sony, wallet=500)
# Wait till the simulation ends
try:
    time.sleep(10)
except KeyboardInterrupt:
    pass

# kill seller thread
seller_apple.kill()
seller_samsung.kill()
seller_sony.kill()

# Plot the sales and expenditure trends
#plot(seller_apple)
#plot(seller_samsung)

#print('Total Profit Apple:', seller_apple.my_profit())
#print('Total Profit Samsung:', seller_samsung.my_profit())

# Kill consumer threads
for consumer in customers:
    consumer.kill()
print ("Done")
sys.exit(0)