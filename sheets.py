import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SPREADSHEET_NAME = "Skylark_Drones"

def get_sheet(sheet_name):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=scope
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open(SPREADSHEET_NAME)
    worksheet = spreadsheet.worksheet(sheet_name)

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df, worksheet