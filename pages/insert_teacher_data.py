import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from google.auth.exceptions import TransportError
from gspread_client import client

st.set_page_config(page_title="Insert Data", layout="wide")
st.title("Insert Teacher Data")
# Step 1: Auth and connect
#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)
#sheet_name="Teacher_Information"
#sheet=client.open("Coaching_Management").worksheet(sheet_name)

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
    name = st.text_input("Name")
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



accessing_sheet_records=sheet.get_all_records()

last_row=accessing_sheet_records[-1]

id=str(last_row["ID"])#accessing specific column name with ID
remaining_part = int(id[1:]) + 1
new_id="T"+str(remaining_part)

# Submit Button
if st.button("Submit"):
    if password==my_password and name.strip() and phone.strip() and institute.strip() and address.strip() and len(phone) ==11 and phone.isdigit():
        Data=[]
        Data.append(name)
        Data.append(new_id)
        Data.append(phone)
        Data.append(institute)
        Data.append(address)
        sheet.append_row(Data)
        st.success(f"Data Submitted Sucessfully and The ID is:{new_id}") 
    elif password!=my_password:
        st.error("Admin Password is not Correct")
    else:
        st.error("Check Phone number  exactly 11 digits and contain only numbers or not. Also check is there any field is empty or not.")