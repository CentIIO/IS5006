import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import os

def update_google_sheet_csv(seller):
    # ## Initialise the client
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credential_file = 'Group4-GoogleSheet-Credential.json'
    client = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(credential_file, scope))

    formatted_seller_name = seller.name.replace(" ","_")
    sheet_file_name = "IS5006_Group4_HW2_" + formatted_seller_name
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
    dict_for_pandas = {}
    dict_for_pandas['Quarter'] = seller.quarter
    for product in seller.products:
        dict_for_pandas['Sales_'+product.name] = seller.sales_history[product]
        dict_for_pandas['Expense_'+product.name] = seller.expense_history[product][1:]
        dict_for_pandas['sentiment_'+product.name] = seller.sentiment_history[product]
    dict_for_pandas['Revenue'] = seller.revenue_history
    dict_for_pandas['Profit'] = seller.profit_history
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

read_from_csv()
