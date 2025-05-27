import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from google.auth.exceptions import TransportError
from gspread_client import client
# Step 1: Auth and connect
#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)


st.set_page_config(page_title="Update Data", layout="wide")
st.title("Update Student Data(Must be Entered ID & Class)")

# First Row
col1, col2 = st.columns(2)
with col1:
    student_id = st.text_input("Student ID")
with col2:
    student_class = st.selectbox(
    "Class:",
    ["6","7","8","9","10","11","12"]
   )

# Second Row
col3, col4 = st.columns(2)
with col3:
    phone = st.text_input("Phone")
with col4:
    institute = st.text_input("Institute")

address = st.text_input("Address")

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


#Accessing the sheet
def making_sheet_name(student_class):
    try:
        sheet_name="Student_Information_Class"+student_class
        return client.open("Coaching_Management").worksheet(sheet_name)
    except TransportError as e:
        st.error("🔌 Network error! Could not connect to Google services. Please check your internet connection and try again.")
        st.stop()
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
        st.stop()



# Submit Button
if st.button("Update"):
    sheet=making_sheet_name(student_class)
    row_num = find_row_by_id(sheet, student_id)
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
            st.success(f"Data updated for ID: {student_id}")
    else:
        st.error("ID not found in the sheet.")
        


#Deleting Student Data
st.title("Delete Student Data")
col1, col2 = st.columns(2)
with col1:
    student_id = st.text_input("Student Id")
with col2:
    student_class = st.selectbox(
    "class:",
    ["6","7","8","9","10","11","12"]
   )

if st.button("Delete"):
    sheet=making_sheet_name(student_class)
    row_num = find_row_by_id(sheet, student_id)
    if row_num:
        sheet.delete_rows(row_num)
        st.success(f"Row with ID {student_id} deleted.")
    else:
        st.error("ID not found in the sheet.")