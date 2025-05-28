import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from google.auth.exceptions import TransportError
from gspread_client import client

st.set_page_config(page_title="Insert Data", layout="wide")
st.title("Update Teacher Data")

# Step 1: Auth and connect
#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)
try:
    sheet_name="Teacher_Information"
    sheet=client.open("Coaching_Management").worksheet(sheet_name)
except TransportError as e:
    st.error("🔌 Network error! Could not connect to Google services. Please check your internet connection and try again.")
    st.stop()
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {e}")
    st.stop()



# First Row
col1, col2 = st.columns(2)
with col1:
    Teacher_id = st.text_input("Teacher ID")
with col2:
    phone = st.text_input("Phone")

# Third Row
col3, col4 = st.columns(2)
with col3:
    institute = st.text_input("Institute")
with col4:
    address = st.text_input("Address")

col5, col6 = st.columns(2)
with col5:
    password = st.text_input("Admin Password",type="password")
#Accessing the password
my_password = st.secrets["password"]



def find_row_by_id(sheet, target_id):
    records = sheet.get_all_records()
    for index, row in enumerate(records):
        if str(row["ID"]) == str(target_id):
            return index + 2  # +2 because of header row and 1-indexing
    return None

# ===== Step 3: Update Only Specific Fields =====
def update_specific_fields(sheet, row_number, updates: dict):
    headers = sheet.row_values(1)
    for key, value in updates.items():
        if key in headers:
            col_number = headers.index(key) + 1
            sheet.update_cell(row_number, col_number, value)
            

if st.button("Submit"):
    if password==my_password:
        row_num = find_row_by_id(sheet, Teacher_id)
        
        if row_num:
            updates={}
            if phone:
                if phone.isdigit() and len(phone)==11:
                    updates["Phone"]=phone
                else:
                    st.warning("Updatation Fail! Due To Phone Length Is Not Equals To 11")
                    st.stop()
            if institute:
                updates["Institute"]=institute
            if address:
                updates["Address"]=address
            if updates:
                update_specific_fields(sheet, row_num, updates)
                st.success(f"Data updated for ID: {Teacher_id}")
        else:
            st.error("ID not found in the sheet.")
    else:
        st.error("Admin Password IS Not Correct!")




st.title("Delete Teacher Data")
col1, col2 = st.columns(2)
with col1:
    Teacher_id = st.text_input("Teacher Id")
with col2:
    password = st.text_input("Admin Password",type="password",key="delete")
#Accessing the password
my_password = st.secrets["password"]

if st.button("Delete"):
    if password==my_password:
        row_num = find_row_by_id(sheet, Teacher_id)
        if row_num:
            sheet.delete_rows(row_num)
            st.success(f"Row with ID {Teacher_id} deleted.")
        else:
            st.error("ID not found in the sheet.")
    else:
        st.error("Admin Password Is Not Correct!")