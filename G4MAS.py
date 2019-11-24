# Authors: Haroon Basheer,Jack Chen and Aman Singhania
# Module:IS5006
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
import platform
import numpy as np


def InitCustomer():
    noCustomers = para.numberofcustomer
    customers = [Customer(name=names.get_full_name(), wallet=np.random.random_integers(500, 1000),
                          type=0.3 + 0.7 * random.random()) for i in range(1, noCustomers + 1)]
    return customers


def main():
    print("[main] import done.")
    # Code to Save the log files in datetime format as per execution
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    # print("date and time =", dt_string)

    if not os.path.exists("log"):
        os.mkdir("log")

    logging.basicConfig(filename=os.path.join("log", dt_string + '.log'), level=logging.INFO)
    random.seed(para.seed)

    # Create Consumer objects based on the number of customers defined in constants file and assign namme, values of wallet and type
    customers = InitCustomer()

    # Construct a product object with following attributes
    iphoneX = Product(name='iphoneX', price=300, quality=0.9, launchtick=5)
    iphone11 = Product(name='iphone11', price=350, quality=0.92)
    galaxy = Product(name='galaxy', price=200, quality=0.8)
    xperia = Product(name='Xperia', price=100, quality=0.6)
    iphoneX_screen = Product(name='iphoneX_screen', price=30, quality=0.9)
    iphoneX_case = Product(name='iphoneX_case', price=30, quality=0.9)
    iphone11_screen = Product(name='iphone11_screen', price=35, quality=0.92)
    iphone11_case = Product(name='iphone11_case', price=35, quality=0.92)
    galaxy_screen = Product(name='galaxy_screen', price=50, quality=0.8)
    galaxy_case = Product(name='galaxy_case', price=30, quality=0.5)
    xperia_screen = Product(name='xperia_screen', price=20, quality=0.8)
    xperia_case = Product(name='xperia_case', price=10, quality=0.7)

    iphone11.add_accessory([iphone11_screen, iphone11_case])
    iphoneX.add_accessory([iphoneX_screen, iphoneX_case])

    galaxy.add_accessory([galaxy_screen, galaxy_case])

    xperia.add_accessory([xperia_screen, xperia_case])

    # Create a Seller object with product as one of the attributes
    seller_apple = Seller(name='APPLE INC', products=[iphoneX, iphone11], wallet=1000)
    seller_samsung = Seller(name='SAMSUNG MOBILES', products=[galaxy], wallet=500)
    seller_sony = Seller(name='SONY INC', products=[xperia], wallet=500)
    # Wait till the simulation ends
    try:
        print("[main] start time.sleep.")
        time.sleep(para.annum_count)
        logging.info('[main]: start killing thread')
    except KeyboardInterrupt:
        pass

    # kill seller thread
    print("[main] start killing sellers thread.")
    seller_apple.kill()
    seller_samsung.kill()
    seller_sony.kill()
    print("[main] sellers thread killed.")

    # Plot the sales and expenditure trends
    # plot(seller_apple)
    # plot(seller_samsung)

    # print('Total Profit Apple:', seller_apple.my_profit())
    # print('Total Profit Samsung:', seller_samsung.my_profit())

    # Kill consumer threads
    for consumer in customers:
        consumer.kill()

    print("[main] start updating google sheet.")
    # from gsheet import update_google_sheet_csv
    # update_google_sheet_csv(seller_apple)
    # update_google_sheet_csv(seller_samsung)
    # update_google_sheet_csv(seller_sony)
    '''
    from gmail import send_gmail
    receiver_address = 'a0197117y.receiver@gmail.com'
    mail_subject = 'A test mail sent by Python.'  # The subject line
    mail_content = ('Hello,\n'
                    'This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.\n'
                    'Thank You\n')
    send_gmail(receiver_address, mail_subject, mail_content)
    
    print ("Done")
    '''
    # sys.exit(0)


def db_init(home_dir=None):
    tar_sys = platform.system()
    home_dir = os.path.expanduser("~")
    if tar_sys == 'Windows':
        db_1 = home_dir + "\Desktop\Customer_SQLite.db"
        db_2 = home_dir + "\Desktop\Seller_SQLite.db"
    elif tar_sys == 'Darwin':
        db_1 = home_dir + "/Desktop/Customer_SQLite.db"
        db_2 = home_dir + "/Desktop/Seller_SQLite.db"
    return db_1, db_2


def customer_dbcreation():
    pass


def seller_dbcreation():
    pass


if __name__ == '__main__':
    tar_sys = platform.system()
    if tar_sys == 'Windows' or 'Darwin':
        customer_db, seller_db = db_init()
        customer_dbcreation()
        seller_dbcreation()

        main()
    else:
        print("Unsupported System")
        sys.exit(0)
