# Authors: Haroon Basheer,Jack Chen and Aman Singhania
# Module:IS5006

#ALL IMPORTS REQUIRED FOR THE EXECUTION OF THE MAS
import logging
import random
import names
import time
import constants as para
from customer import Customer
from product import Product
from seller import Seller

#ALL VISUALIZATIONS HAVE BEEN DONE USING MICROSOFT POWER BI

import os
from datetime import datetime
import sys
import platform
import numpy as np

# USE THIS IMPORT TO CONNECT WITH THE MYSQL LITE DATABASE
import Database as Db
import pandas as pd
from gsheet import update_google_sheet_csv

# THE DATA STRUCTURE OF LISTS HAS BEEN USED TO SAVE THE PRODUCTS AND SELLERS RESPECTIVELY
products = []
sellers=[]

# THE DATA STRUCTURE OF SETS HAS BEEN USED TO SAVE THE COMPANY AND THE PRODUCTS OFFERED RESPECTIVELY
company = set()
company_prd={}

# INITIALIZATION OF CUSTOMERS
def InitCustomer():

    # THE noCustomer IS A CONSTANT THAT CAN BET SET IN THE constants.py FILE
    # IT DENOTES THE NUMBER OF CUSTOMERS BEING SERVED BY THE MAS
    noCustomers = para.numberofcustomer

    # INITIALIZATION OF CUSTOMERS WITH THE ATTRIBUTES OF WALLET, TYPE AND NAME.
    customers = [Customer(name=names.get_full_name(), wallet=np.random.random_integers(500, 1000),
                          type=0.3 + 0.7 * random.random()) for i in range(1, noCustomers + 1)]
    return customers

# INITIALIZATION OF THE LOG FILE. LOG FILE HAS BEEN USED TO UNDERSTAND PROGRAM FLOW
def InitLog():
    # THE LOG FILE IS SAVED WITH THE TIMESTAMP VALUE WHENEVER THE MAS IS EXECUTED.
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists("log"):
        os.mkdir("log")
    logging.basicConfig(filename=os.path.join("log", dt_string + '.log'), level=logging.INFO)
    random.seed(para.seed)

# READING AND THEN INITIALIZATION OF THE PRODUCTS WITH THE CONTENTS OF THE CSV FILE.
def InitProducts():
    ProdData = pd.read_csv("./Products.csv")
    for i in range(0, len(ProdData)):
        products.append(Product(name=ProdData.iloc[i]['Name'],
                                price=ProdData.iloc[i]['Price'],
                                quality=ProdData.iloc[i]['Quality'],
                                launchtick=ProdData.iloc[i]['Launch ']
                                )
                        )
        company.add(str(ProdData.iloc[i]['Company']))

    # BUNDLING THE MAIN PRODUCT WITH EACH OF ITS ACCESSORIES
    for i in range(0, len(ProdData)):
        x=[]
        y = str(ProdData.iloc[i]['Related Items'])
        x = y.split(",")
        for product in products:
            if ProdData.iloc[i]['Name']==product.name:
                main_prod=product
        for items in range(0, len(x)):
            main_prod_access=[]
            for product in products:
                if x[items]==product.name:
                    main_prod_access.append(product)
        main_prod.add_accessory(main_prod_access)

    # INITIALIZING THE COMPANIES WITH THE CONTENTS OF THE CSV FILE.
    for val in company:
        test = []
        for i in range(0, len(ProdData)):
            if val==str(ProdData.iloc[i]['Company']):
                for product in products:
                    if product.name==ProdData.iloc[i]['Name'] and ProdData.iloc[i]['Related Items']!='-':
                        test.append(product)
                    company_prd[ProdData.iloc[i]['Company']]=test
        sellers.append(Seller(name=val,
                              products=test,
                              wallet=1000
                              )
                        )

# THE MAIN METHOD
def main():

    # WE MAKE THE CALL FOR EACH OF THE INITIALIZATION FUNCTIONS
    InitLog()
    customers = InitCustomer()
    InitProducts()
    try:
        # SLEEP METHOD OF THREAD
        print("[main] start time.sleep.")
        time.sleep(para.annum_count)
        logging.info('[main]: start killing thread')
    except KeyboardInterrupt:
        pass

    # KILL SELLER THREAD

    print("[main] start killing sellers thread.")
    for seller in sellers:
        seller.kill()

    print("[main] sellers thread killed.")

    # KILL CONSUMER THREAD
    for consumer in customers:
        consumer.kill()

    print("[main] start updating google sheet.")

    # UPDATING GOOGLE SHEET WITH ALL THE SELLER INFORMATION
    for seller in sellers:
        update_google_sheet_csv(seller)

# CREATING THE DATABASE FILE
if __name__ == '__main__':
    tar_sys = platform.system()
    if tar_sys == 'Windows' or 'Darwin':
        MAS_db = Db.db_init()
        Db.customer_dbcreation(MAS_db)

        main()
    else:
        print("Unsupported System")
        sys.exit(0)
