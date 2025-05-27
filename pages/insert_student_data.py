import json
import streamlit as st
from google.oauth2 import service_account
import gspread
from gspread_client import client
#scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials JSON string from Streamlit secrets
#service_account_json_str = st.secrets["GOOGLE_CREDENTIALS"]

# Parse JSON string into a dict
#service_account_info = json.loads(service_account_json_str)

# Create credentials object
#credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=scope)

# Authorize gspread
#client = gspread.authorize(credentials)

# Step 1: Auth and connect
#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)
st.set_page_config(page_title="Insert Data", layout="wide")
st.title("Insert Student Data")

# First Row
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name")
with col2:
    student_class = st.selectbox(
    "Class:",
    ["6","7","8","9","10","11","12"]
   )

# Second Row
col3, col4 = st.columns(2)
with col3:
    guardian_name = st.text_input("Guardian Name")
with col4:
    phone = st.text_input("Phone")

# Third Row
col5, col6 = st.columns(2)
with col5:
    institute = st.text_input("Institute")
with col6:
    address = st.text_input("Address")

col7, col8 = st.columns(2)
with col7:
    group = st.selectbox(
    "Group:",
    ["None","Science","Commerce","Arts"]
   )
with col8:
    amount = st.text_input("Amount")
#Accesing the sheet
sheet_name="Student_Information_Class"+student_class

sheet = client.open("Coaching_Management").worksheet(sheet_name)

accessing_sheet_records=sheet.get_all_records()

last_row=accessing_sheet_records[-1]

id=str(last_row["ID"])#accessing specific column name with ID

if len(student_class) ==1:
    remaining_part = int(id[1:]) + 1
else:
     remaining_part = int(id[2:]) + 1  
      
new_id = int(student_class + str(remaining_part))
# Submit button only shown when every filled are fillup
if st.button("Submit"):
    if name.strip() and student_class.strip() and amount.strip() and guardian_name.strip() and phone.strip() and institute.strip() and address.strip() and group.strip() and len(phone) ==11 and phone.isdigit():
            Data=[]
            Data.append(name)
            Data.append(new_id)
            Data.append(student_class)
            Data.append(guardian_name)
            Data.append(phone)
            Data.append(institute)
            Data.append(address)
            Data.append(group)
            Data.append(amount)
            sheet.append_row(Data)
            st.success(f"Data Submitted Sucessfully and The ID is:{new_id}")
    else:
        st.error("Check Phone number  exactly 11 digits and contain only numbers or not. Also check is there any field is empty or not.")
