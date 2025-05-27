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

st.set_page_config(layout="wide")

st.title("Student Information Lookup")


def find_last_row_by_id(sheet, target_id):
    records = sheet.get_all_records()
    row_num=0
    for idx, row in enumerate(records, start=2):  # start=2 because row 1 is the header
        if str(row["ID"]) == str(target_id):
            row_num =idx  # Google Sheets is 1-indexed
    return row_num





# Input Section
st.subheader("Search Student")
col1, col2 = st.columns(2)
col1, col2 = st.columns(2)
with col1:
    student_id = st.text_input("Student ID")
with col2:
    student_class = st.selectbox(
    "Class:",
    ["6","7","8","9","10","11","12"]
   )
    

st.write("(If You Want to See Individual Result Then Fill The Student ID Otherwise Don't Do Anything)")
col3, col4 = st.columns(2)
with col3:
    option = st.selectbox(
    "Select your class:",
    ["Individual","All","Unpaid"]
   )


def find_row_by_id(sheet, target_id):
    records = sheet.get_all_records()
    for index, row in enumerate(records):
        if str(row["ID"]) == str(target_id):
            return index + 2  # +2 because of header row and 1-indexing
    return None



#Student Basic Information
#sheet_name="Student_Information_Class"+student_class
#sheet = client.open("Coaching_Management").worksheet(sheet_name)
#row_num = find_row_by_id(sheet, student_id)
#Student Salary Information
#sheet_name="Student_Salary_information_Class"+student_class
#sheet1 = client.open("Coaching_Management").worksheet(sheet_name)

try:
    sheet_name="Student_Information_Class"+student_class
    sheet = client.open("Coaching_Management").worksheet(sheet_name)
    sheet_name="Student_Salary_information_Class"+student_class
    sheet1 = client.open("Coaching_Management").worksheet(sheet_name)
except TransportError as e:
    st.error("🔌 Network error! Could not connect to Google services. Please check your internet connection and try again.")
    st.stop()
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {e}")
    st.stop()






row_num = find_row_by_id(sheet, student_id)
row_num1 = find_last_row_by_id(sheet1, student_id)
#Declaring the variable
name = ""
g_name = ""
phone = ""
institute = ""
address=""
group = ""
amount=""
month=""
#st.write(row_num)
#st.write(row_num1)
# Submit Button
if st.button("Submit"):
    if option=="Individual":
        if row_num and row_num1:
            headers = sheet.row_values(1)
            row_data = sheet.row_values(row_num)
            row_dict = dict(zip(headers, row_data))
            name = row_dict.get("Name", "")
            g_name = row_dict.get("Guardian Name", "")
            phone = row_dict.get("Phone", "")
            institute = row_dict.get("Institute", "")
            address=row_dict.get("Address", "")
            group = row_dict.get("Group", "")
        #accessing the salary sheet
            headers = sheet1.row_values(1)
            row_data = sheet1.row_values(row_num1)
            row_dict = dict(zip(headers, row_data))
            amount = row_dict.get("Amount", "")
            month = row_dict.get("Month", "")
        else:
            st.error("Id not found")
            st.stop()

        
 



        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Name", value=name, disabled=True)
        with col2:
            st.text_input("ID", value=student_id, disabled=True)

        col3, col4 = st.columns(2)
        with col3:
            st.text_input("Class", value=student_class, disabled=True)
        with col4:
            st.text_input("Institute", value=institute, disabled=True)

        col5, col6 = st.columns(2)
        with col5:
            st.text_input("Guardian Name", value=g_name, disabled=True)
        with col6:
            st.text_input("Phone", value=phone, disabled=True)

        col7, col8 = st.columns(2)
        with col7:
            st.text_input("Address", value=address, disabled=True)
        with col8:
            st.text_input("Last Payment", value=month, disabled=True)
        
        col9, col10 = st.columns(2)
        with col9:
            st.text_input("Payment Take",value=amount,disabled=True)
        with col10:
            st.text_input("Group",value=group,disabled=True)
    if option=="All":
        data = sheet.get_all_records()
        if data:
            df = pd.DataFrame(data)
            df = df.drop(index=0).reset_index(drop=True)
        else:
            st.warning("The Sheet is Empty!")
            st.stop()
        st.markdown(
               """
               <style>
                   table {
                       width: 100%;
                       text-align: center !important;
                   }
                   th, td {
                   text-align: center !important;
                   }
               </style>
               """,
               unsafe_allow_html=True
           )
        st.table(df) 

    if option=="Unpaid":
        data = sheet1.get_all_records()
        
        if data:
            df = pd.DataFrame(data)
            df = df.groupby('ID', as_index=False).last()
        else:
            st.warning("The Sheet is Empty!")
            st.stop()
        #df = df.drop(index=0).reset_index(drop=True)
        #st.dataframe(df)
        st.markdown(
               """
               <style>
                   table {
                       width: 100%;
                       text-align: center !important;
                   }
                   th, td {
                   text-align: center !important;
                   }
               </style>
               """,
               unsafe_allow_html=True
           )
        st.table(df) 