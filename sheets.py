import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SPREADSHEET_ID = "1MYJxd2UZQptgUF0UVDDUwCB1WNh1gpsXPcBzzzk7PSc"

def get_sheet(tab_name):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.worksheet(tab_name)

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df, worksheet
