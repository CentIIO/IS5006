import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import os
import constants as const

#trim ngram product relation array
def trim(count,list):
    rep=int(len(list)/count)
    loc=0
    temp=0
    list2=[]
    for i in range(0,count):
        for j in range(0,rep):
            temp+=list[loc]
            loc+=1
        list2.append(temp)
        temp=0
    return list2
def update_google_sheet_csv(seller):
    # ## Initialise the client
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credential_file = 'Group4-GoogleSheet-Credential.json'
    client = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(credential_file, scope))

    formatted_seller_name = seller.name.replace(" ","_")
    sheet_file_name = "IS5006_G4_MAS" + formatted_seller_name
    print("sheet_file_name:",sheet_file_name)

    # ### Try to open the sheet. If it does not exist, create and share it.
    try:
        sheet = client.open(sheet_file_name)
        print("sheet open successfully.")
    except gspread.exceptions.SpreadsheetNotFound:
        print("Google sheet not exist, create and share it.")
        sheet = client.create(sheet_file_name)
        sheet.share('a0197117y.receiver@gmail.com', perm_type='user', role='writer')

    # ### Selecting a worksheet
    # worksheet = sheet.worksheet("Sheet1")

    # clear the worksheet
    # worksheet.clear()

    # export data to csv and import to populate google sheet
    csv_path = os.path.join("log",formatted_seller_name + '_Data.csv')
    print(csv_path)
    dict_for_pandas = {}
    dict_for_pandas['Month'] = seller.month
    dict_for_pandas['Revenue'] = seller.revenue_history
    dict_for_pandas['Total_expense'] = seller.total_expense_history[1:]
    dict_for_pandas['Profit'] = seller.profit_history
    dict_for_pandas['Total_sales'] = seller.total_sales_history
    dict_for_pandas['Wallet'] = seller.wallet_history
    for product in seller.products:
        dict_for_pandas['Inventory_' + product.name] = seller.inventory_history[product]
        dict_for_pandas['Price_' + product.name] = seller.price_history[product]
        #bug
        print("====")
        print(product.name)
        print(seller.sales_history[product])
        print("+++++++")
        dict_for_pandas['Sales_'+product.name] = seller.sales_history[product]
        dict_for_pandas['Expense_'+product.name] = seller.expense_history[product][1:]
        dict_for_pandas['sentiment_'+product.name] = seller.sentiment_history[product]
        dict_for_pandas['Ad_type_' + product.name] = seller.adverts_type_history[product]
        dict_for_pandas['Ad_scale_' + product.name] = seller.adverts_scale_history[product]

    #bug
    for product in seller.accessaries:
        templist=[]
        #length=len(seller.sales_history[product])
        print("length^^",len(seller.sales_history[product]))
        if len(seller.sales_history[product])==const.annum_count+1:
            dict_for_pandas['Sales_' + product.name] = seller.sales_history[product]
        else:

            trimmed=trim(len(seller.month),seller.sales_history[product])
            dict_for_pandas['Sales_' + product.name] = trimmed
              #for i in range(0,)


    print(dict_for_pandas)
    for k,v in dict_for_pandas.items():
        print("key:",k,"value length:",len(v))
    pandas.DataFrame(dict_for_pandas).to_csv(csv_path, mode = 'w', index=False)
    # pandas.DataFrame({'Sales': seller.sales_history,
    #                   'Revenue': seller.revenue_history,
    #                   'Profit': seller.profit_history,
    #                   'Expense': seller.expense_history[1:],
    #                   'Sentiment': seller.sentiment_history}).to_csv(csv_path, mode='w', index=False)

    content = open(csv_path, 'r').read()
    client.import_csv(sheet.id, content)

def read_from_csv():
    import csv

    with open('log\\APPLE_INC_Data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]}  {row[1]} {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')

