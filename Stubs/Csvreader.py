class Product(object):
    def __init__(self, name):
        self.name = name
        self.price=1
        self.quantity=0
        self.quality=1
        self.launchtick=0
        self.company=None
        self.relatedProd=[]
        
    def getName(self):
        return self.name
    
    def setPrice(self,price):
        self.price=price
        
    def getPrice(self):
        return self.price
 
    def setquantity(self,quantity):
        self.quantity=quantity
    
    def getquantity(self):
        return self.quantity
    
    def setquality(self,quality):
        self.quality=quality
    
    def getquality(self):
        return self.quality
    
    def setlaunchtick(self,launchtick):
        self.launchtick=launchtick
    
    def getlaunchtick(self):
        return self.launchtick
    
    def setcompany(self,company):
        self.company=company
    
    def getcompany(self):
        return self.company
        

    def setrelatedProd(self,relatedProd):
        self.relatedProd.append(relatedProd)
        
    def getrelatedProd(self):
        return self.relatedProd 





# importing csv module 
import csv 
  
# csv file name 
filename = "Products.csv"
  
# initializing the titles and rows list 
fields = [] 
rows = [] 
  
# reading csv file 
with open(filename, 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
      
    # extracting field names through first row 
    fields = next(csvreader)
  
    # extracting each data row one by one 
    for row in csvreader: 
        rows.append(row) 
  
    # get total number of rows 
    #print("Total no. of rows: %d"%(csvreader.line_num)) 
  
# printing the field names 
#print('Field names are:' + ', '.join(field for field in fields)) 
#print (len(fields))
for field in fields:
    #print (field)
    pass

  
#  printing first 5 rows 

for row in rows[:-1]: 
    # parsing each column of a row 
    for col in row: 
        content=[]
        content=col
        #print (content)
        #print("%10s"%col), 
    #print('\n') 
    
import csv
from collections import defaultdict

columns = defaultdict(list) # each value in each column is appended to a list

with open('Products.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list

Item=[]  # based on column name k
prod_count=0
company=set()
for field in fields:
    prod_count=len(columns[field])
    if field=='Name':
        for j in range(0,prod_count):
            Item.append(columns[field][j])
            #print(columns[field][j])
            Item[j]=Product(columns[field][j])
            #print (Item[j].getName())
    elif field=='Price':
            for j in range(0,prod_count):
            #Item.append(columns[field][j])
                #print(columns[field][j])
                Item[j].setPrice(columns[field][j])
                #print (Item[j].getPrice())         
    elif field=='Quantity':
            for j in range(0,prod_count):
            #Item.append(columns[field][j])
                #print(columns[field][j])
                Item[j].setquantity(columns[field][j])
                #print (Item[j].getquantity())    
    elif field=='Quality':
            for j in range(0,prod_count):
            #Item.append(columns[field][j])
                #print(columns[field][j])
                Item[j].setquality(columns[field][j])
                #print (Item[j].getquality())  
    elif field=='Launch':
            for j in range(0,prod_count):
            #Item.append(columns[field][j])
                #print(columns[field][j])
                Item[j].setlaunchtick(columns[field][j])
                #print (Item[j].getlaunchtick())
    elif field=='Company':
            for j in range(0,prod_count):
            #Item.append(columns[field][j])
                #print(columns[field][j])
                Item[j].setcompany(columns[field][j])
                company.add(columns[field][j])
                #print (Item[j].getlaunchtick())
                
                
for field in fields:              
    if field=='Related Items':
            for j in range(0,prod_count):
                print (Item[j].getName())
                #for each product list in the csv get the related item and store it in a list
                relatedprod=columns[field][j].split(",")
                print (relatedprod)
                #get the object from the product list
                for relitem in relatedprod:
                    #for all the items in the product
                    for prod in range(0,prod_count):
                        #if the product object  matches the related item
                        if(Item[prod].getName()==relitem):
                                #append the current related item object to the product
                                Item[j].setrelatedProd(Item[prod])   

                                
tester=[]
for j in range(0,prod_count):  
    tester=Item[j].getrelatedProd()  
    print ("printing related item name for",Item[j].getName())
    for i in tester:
        print (i.getName())
        print (i.getPrice())
    
    
for j in range(0,prod_count):
    print(Item[j].getName(),",",Item[j].getcompany(),",",Item[j].getrelatedProd())

    
c1=str(Item[0].getcompany())
if c1=='Apple':
    print ("Apple")
    
print(company)
