#task for assignment:
'''draw the flowchart and export metrics to google sheets'''

#author: HB,Jack Shen
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

if not os.path.exists("log"):
    os.mkdir("log")

logging.basicConfig(filename=os.path.join("log",dt_string+'.log'), level=logging.INFO)
random.seed(para.seed)
#'consumer_' + str(i)
# Create 500  Consumers objects and assign initial with tolerance and wallet 
customers = [Customer(name=names.get_full_name(), wallet=500,tolerance=0.5 + 0.4 * random.random() ) for i in range(1,(para.numberofcustomer+1))]


# Construct a product object with following attributes
iphoneX = Product(name='iphoneX', price=300, quality=0.9)
iphone11 = Product(name='iphone11', price=350, quality=0.92)
galaxy = Product(name='Note', price=200, quality=0.8)
sony = Product(name='Xperia', price=100, quality=0.6)

# Create a Seller object with product as one of the attributes
seller_apple = Seller(name='APPLE INC', products=[iphoneX, iphone11], wallet=1000)
seller_samsung = Seller(name='SAMSUNG MOBILES', products=[galaxy], wallet=500)
seller_sony = Seller(name='SONY', products=[sony], wallet=500)
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

print("[main] start updating google sheet.")
from gsheet import update_google_sheet_csv
update_google_sheet_csv(seller_apple)
update_google_sheet_csv(seller_samsung)
update_google_sheet_csv(seller_sony)

print ("Done")
sys.exit(0)