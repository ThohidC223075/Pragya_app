import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime
from gspread_client import client

# Step 1: Auth and connect
#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)
sheet_name="Teacher_Taken_Class_Information"
sheet=client.open("Coaching_Management").worksheet(sheet_name)


st.set_page_config(page_title="Attendance", layout="wide")
st.title("Attendance For Taken Class")

# First Row
paid="No"

col1, col2 = st.columns(2)
with col1:
    teacher_id = st.text_input("Teacher ID")
with col2:
    selected_date = st.date_input("Select Date", datetime.date.today())

# Third Row
col3, col4 = st.columns(2)
with col3:
    class6 = st.text_input("Class 6")
with col4:
    class7 = st.text_input("Class 7")
    
col5, col6 = st.columns(2)
with col5:
    class8 = st.text_input("Class 8")
with col6:
    class9 = st.text_input("Class 9")
    
col7, col8 = st.columns(2)
with col7:
    class10 = st.text_input("Class 10")
with col8:
    class11 = st.text_input("Class 11")

col9, col10 = st.columns(2)
with col9:
    class12 = st.text_input("Class 12")
with col10:
    t_password = st.text_input("Teacher Password",type="password")
#Accessing the password
teacher_password = st.secrets["teacher_password"]

if st.button("Submit"):
    if t_password==teacher_password:
        Data=[]
        Data.append(teacher_id)
        Data.append(str(selected_date ))
        Data.append(class6 if class6 else "0")
        Data.append(class7 if class7 else "0")
        Data.append(class8 if class8 else "0")
        Data.append(class9 if class9 else "0")
        Data.append(class10 if class10 else "0")
        Data.append(class11 if class11 else "0")
        Data.append(class12 if class12 else "0")
        Data.append(paid)
        sheet.append_row(Data)
        st.success("Data Submitted Successfully!")
    else:
        st.error("Teacher Password Is Not Correct!")




#Updating the class

def find_row_by_id(sheet, target_id,date):
    records = sheet.get_all_records()
    for index, row in enumerate(records):
        if str(row["ID"]) == str(target_id) and str(row["Date"])==date:
            return index + 2  # +2 because of header row and 1-indexing
    return None

# ===== Step 3: Update Only Specific Fields =====
def update_specific_fields(sheet, row_number, updates: dict):
    headers = sheet.row_values(1)
    for key, value in updates.items():
        if key in headers:
            col_number = headers.index(key) + 1
            sheet.update_cell(row_number, col_number, value)


st.title("Update If Any Mistake Are Happened")

# First Row
col1, col2 = st.columns(2)
with col1:
    teacher_id = st.text_input("Teacher Id")
with col2:
    selected_date = st.date_input("Select date", datetime.date.today())

# Third Row
col3, col4 = st.columns(2)
with col3:
    classVI = st.text_input("Class VI")
with col4:
    classVII = st.text_input("Class VII")
    
col5, col6 = st.columns(2)
with col5:
    classVIII = st.text_input("Class VIII")
with col6:
    classIX = st.text_input("Class IX")
    
col7, col8 = st.columns(2)
with col7:
    classX = st.text_input("Class X")
with col8:
    classXI = st.text_input("Class XI")

col9, col10 = st.columns(2)
with col9:
    classXII = st.text_input("Class XII")
with col10:
    t_password = st.text_input("Teacher Password",type="password",key="update")


if st.button("Update"):
    if t_password==teacher_password:
        row_num = find_row_by_id(sheet, teacher_id,str(selected_date))
        if row_num:
            updates={}
            if classVI:
                updates["Class-6"]=classVI
            if classVII:
                updates["Class-7"]=classVII
            if classVIII:
                updates["Class-8"]=classVIII
            if classIX:
                updates["Class-9"]=classIX
            if classX:
                updates["Class-10"]=classX
            if classXI:
                updates["Class-11"]=classXI
            if classXI:
                updates["Class-12"]=classXII
            if updates:
                update_specific_fields(sheet, row_num, updates)
                st.success(f"Data updated for ID: {teacher_id}")
                
        else:
            st.error("No Data Found!")
    else:
        st.error("Teacher Password Is Not Correct!")