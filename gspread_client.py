import json
import streamlit as st
import gspread
from google.oauth2 import service_account

# Define scopes
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit secrets
service_account_json_str = st.secrets["GOOGLE_CREDENTIALS"]
service_account_info = json.loads(service_account_json_str)

# Create credentials
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=scope)

# Authorize and create gspread client
client = gspread.authorize(credentials)
