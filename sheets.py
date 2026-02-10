import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SPREADSHEET_NAME = "Skylark_Drones"  # EXACT Google Sheet name

def get_sheet(sheet_name):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # ✅ READ CREDENTIALS FROM STREAMLIT SECRETS
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open(SPREADSHEET_NAME)
    worksheet = spreadsheet.worksheet(sheet_name)

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df, worksheet
