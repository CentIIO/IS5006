import platform
import os
import sqlite3
from sqlite3 import Error




# CREATE THE DATABASE FILE IN THE DESKTOP OF THE LOCAL MACHINE BASED ON THE OS
def db_init():
    tar_sys = platform.system()
    home_dir = os.path.expanduser("~")
    if tar_sys == 'Windows':
        db_1 = home_dir + "\Desktop\MAS_SQLite.db"
    elif tar_sys == 'Darwin':
        db_1 = home_dir + "/Desktop/MAS_SQLite.db"
    return db_1

# CREATE TWO TABLES IN THE DB AS CUSTOMER AND SELLER

def customer_dbcreation(G4MAS_db):
    G4MAS_DBconn = None
    try:
        G4MAS_DBconn = sqlite3.connect(G4MAS_db)
        sql_create_customer_table = """ CREATE TABLE IF NOT EXISTS Customer (
                                            id integer PRIMARY KEY,
                                            name text,
                                            wallet text,
                                            type real
                                        ); """
        sql_create_seller_table = """ CREATE TABLE IF NOT EXISTS Seller (
                                            id integer PRIMARY KEY,
                                            Seller_Name text,
                                            Products text,
                                            Accessories text,
                                            Wallet text
                                        ); """
        # conn,sql_create_customer_table

        c = G4MAS_DBconn.cursor()
        c.execute(sql_create_customer_table)
        c.execute(sql_create_seller_table)


    except Error as e:
        print(e)

# UPDATE THE CUSTOMER DATABASE

def update_CustDB(name,wallet,type):
        try:
            test=(name,wallet,type)
            #conn = sqlite3.connect(db_file)
            G4MAS_DBconn = sqlite3.connect(db_init())
            with G4MAS_DBconn:
                sql = '''INSERT INTO Customer(name,wallet,type)
                      VALUES(?,?,?) '''
                cur = G4MAS_DBconn.cursor()
                cur.execute(sql,test)

            #return cur.lastrowid
            #print ("db updated")
        except Error as e:
            print(e)

# UPDATE THE SELLER DATABASE

def update_SellerDB(name,product,accessories,wallet):
    try:
        test = (name,product,accessories,wallet)
        # conn = sqlite3.connect(db_file)
        G4MAS_DBconn = sqlite3.connect(db_init())
        with G4MAS_DBconn:
            sql = '''INSERT INTO Seller(Seller_Name,Products,Accessories,Wallet)
                  VALUES(?,?,?,?) '''
            cur = G4MAS_DBconn.cursor()
            cur.execute(sql, test)

        # return cur.lastrowid
        # print ("db updated")
    except Error as e:
        print(e)
