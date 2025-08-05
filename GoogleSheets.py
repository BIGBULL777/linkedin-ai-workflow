# sheets.py
import gspread
from gspread import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pandas import DataFrame

# sheets.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads from .env

# sheets.py

import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet(sheet_name: str, worksheet_index: int = 0, GOOGLE_CREDS_PATH: str = None):
    if GOOGLE_CREDS_PATH is None:
        GOOGLE_CREDS_PATH = os.getenv("GOOGLE_CREDS_PATH")

    if not GOOGLE_CREDS_PATH:
        raise ValueError("GOOGLE_CREDS_PATH is not set. Make sure .env file is loaded and contains the correct key.")

    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS_PATH, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).get_worksheet(worksheet_index)
    return sheet



def read_sheet_as_df(sheet_name: str) -> tuple[DataFrame, Worksheet]:
    sheet = get_sheet(sheet_name)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df, sheet


def update_sheet_row(sheet, row_index: int, content: str):
    sheet.update_cell(row_index + 2, 6, content)
