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
import Database as Db
import pandas as pd

products = []
sellers=[]
company = set()
bundling=set()
company_prd={}


def InitCustomer():
    noCustomers = para.numberofcustomer
    customers = [Customer(name=names.get_full_name(), wallet=np.random.random_integers(500, 1000),
                          type=0.3 + 0.7 * random.random()) for i in range(1, noCustomers + 1)]
    return customers


def InitLog():
    # Code to Save the log files in datetime format as per execution
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists("log"):
        os.mkdir("log")
    logging.basicConfig(filename=os.path.join("log", dt_string + '.log'), level=logging.INFO)
    random.seed(para.seed)


def InitProducts():
    ProdData = pd.read_csv("./Products2.csv")
    for i in range(0, len(ProdData)):
        products.append(Product(name=ProdData.iloc[i]['Name'],
                                price=ProdData.iloc[i]['Price'],
                                quality=ProdData.iloc[i]['Quality'],
                                launchtick=ProdData.iloc[i]['Launch ']
                                )
                        )
        company.add(str(ProdData.iloc[i]['Company']))

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

    #find the company
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


def main():
    InitLog()
    # Create Consumer objects based on the number of customers defined in constants file and assign namme, values of wallet and type
    customers = InitCustomer()
    InitProducts()



    try:
        print("[main] start time.sleep.")
        time.sleep(para.annum_count)
        logging.info('[main]: start killing thread')
    except KeyboardInterrupt:
        pass

    # kill seller thread

    print("[main] start killing sellers thread.")
    for seller in sellers:
        seller.kill()

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

    from gsheet import update_google_sheet_csv

    for seller in sellers:
        update_google_sheet_csv(seller)


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


if __name__ == '__main__':
    tar_sys = platform.system()
    if tar_sys == 'Windows' or 'Darwin':
        MAS_db = Db.db_init()
        Db.customer_dbcreation(MAS_db)

        main()
    else:
        print("Unsupported System")
        sys.exit(0)
