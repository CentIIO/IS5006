# NOT NEEDED
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import os

def delete_google_sheet(sheet_file_name):
    # ## Initialise the client
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credential_file = 'Group4-GoogleSheet-Credential.json'
    client = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(credential_file, scope))


    # sheet_file_name = "IS5006_Group4_HW2_APPLE_INC"
    print("sheet_file_name:",sheet_file_name)

    # ### Create a sheet. if sheet is already created, comment out it
    # sheet = client.create(sheet_file_name)

    # ### Open a spreadsheet file
    try:
        sheet = client.open(sheet_file_name)
        client.del_spreadsheet(sheet.id)
    except gspread.exceptions.SpreadsheetNotFound:
        print("exception triggered")
        print("2nd row exception")
    print("done")

delete_google_sheet("IS5006_Group4_HW2_APPLE_INC")
delete_google_sheet("IS5006_Group4_HW2_SAMSUNG_MOBILES")
delete_google_sheet("IS5006_Group4_HW2_SONY_INC")

def test_list_sum():
    a = [[1,1],[2,2],[3,4]]
    b = [x[1] for x in a]
    print("b:",b)
    print("b sum:",sum(b))

# test_list_sum()

def test_dict_sum():
    a = {"a":1,
         "b":2,
         "c":4}
    b = [v for k,v in a.items()]
    print("b:",b)

# test_dict_sum()
