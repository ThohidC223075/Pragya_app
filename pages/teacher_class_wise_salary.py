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
sheet_name="Teacher_Class_Wise_Salary"
sheet=client.open("Coaching_Management").worksheet(sheet_name)

try:
    sheet_name="Teacher_Class_Wise_Salary"
    sheet=client.open("Coaching_Management").worksheet(sheet_name)
except TransportError as e:
    st.error("🔌 Network error! Could not connect to Google services. Please check your internet connection and try again.")
    st.stop()
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {e}")
    st.stop()





st.set_page_config(page_title="Salary", layout="wide")
st.title("Teacher Class Wise Salary")

# First Row
col1, col2 = st.columns(2)
with col1:
    teacher_id = st.text_input("Teacher ID")
with col2:
    class6 = st.text_input("Class 6")
# Third Row
col3, col4 = st.columns(2)
with col3:
    class7 = st.text_input("Class 7")
with col4:
    class8 = st.text_input("Class 8")
    
col5, col6 = st.columns(2)
with col5:
    class9 = st.text_input("Class 9")
with col6:
    class10 = st.text_input("Class 10")
    
col7, col8 = st.columns(2)
with col7:
    class11 = st.text_input("Class 11")
with col8:
    class12 = st.text_input("Class 12")

if st.button("Submit"):
    Data=[]
    Data.append(teacher_id)
    Data.append(class6 if class6 else "0")
    Data.append(class7 if class7 else "0")
    Data.append(class8 if class8 else "0")
    Data.append(class9 if class9 else "0")
    Data.append(class10 if class10 else "0")
    Data.append(class11 if class11 else "0")
    Data.append(class12 if class12 else "0")
    sheet.append_row(Data)
    st.success("Data Submitted Successfully!")


#Update Class wise salary
st.title("Update Class Wise Salary")

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

col1, col2 = st.columns(2)
with col1:
    teacher_id = st.text_input("Teacher Id")
with col2:
    classVI = st.text_input("Class VI")
    
col3, col4 = st.columns(2)
with col3:
    classVII = st.text_input("Class VII")
with col4:
    classVIII = st.text_input("Class VIII")
    
col5, col6 = st.columns(2)
with col5:
    classIX = st.text_input("Class IX")
with col6:
    classX = st.text_input("Class X")
    
col7, col8 = st.columns(2)
with col7:
    classXI = st.text_input("Class XI")
with col8:
    classXII = st.text_input("Class XII")



if st.button("Update"):
    row_num = find_row_by_id(sheet, teacher_id)
    if row_num:
        updates={}
        if classVI:
            updates["Amount-6"]=classVI
        if classVII:
            updates["Amount-7"]=classVII
        if classVIII:
            updates["Amount-8"]=classVIII
        if classIX:
            updates["Amount-9"]=classIX
        if classX:
            updates["Amount-10"]=classX
        if classXI:
            updates["Amount-11"]=classXI
        if classXII:
            updates["Amount-12"]=classXII
        if updates:
            update_specific_fields(sheet, row_num, updates)
            st.success(f"Data updated for ID: {teacher_id}")
            
    else:
        st.error("ID Not Found!")