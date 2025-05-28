import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import urllib.parse
from datetime import datetime
from google.auth.exceptions import TransportError
from gspread_client import client
st.set_page_config(page_title="Insert Data", layout="wide")
st.title("Insert Student Data")
# Step 1: Auth and connect
#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)

# First Row
col1, col2 = st.columns(2)
with col1:
    Id = st.text_input("ID")
with col2:
    month = st.text_input("Month")

# Second Row
col3, col4 = st.columns(2)
with col3:
    actual_amount = st.text_input("Actual Amount")
with col4:
    duplicate_amount = st.text_input("Duplicate Amount")
col5, col6 = st.columns(2)
with col5:
    student_class = st.selectbox(
    "Class:",
    ["6","7","8","9","10","11","12"]
   )
with col6:
    author=st.selectbox(
        "Received By",
        ["Director","Manager","Owner"]
    )
    
col7, col8 = st.columns(2)
with col7:
    password = st.text_input("Admin Password",type="password")
#Accessing the password
my_password = st.secrets["password"]


try:
    sheet_name="Student_Salary_information_Class"+student_class
    sheet = client.open("Coaching_Management").worksheet(sheet_name)
except TransportError as e:
    st.error("🔌 Network error! Could not connect to Google services. Please check your internet connection and try again.")
    st.stop()
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {e}")
    st.stop()


# Submit button only shown when every filled are fillup

if st.button("Submit"):
    if password==my_password:
        if Id.strip() and month.strip() and actual_amount.strip() and duplicate_amount.strip():
            current_date = datetime.today().date()
            Data=[]
            Data.append(Id)
            Data.append(actual_amount)
            Data.append(month)
            Data.append(str(current_date))
            sheet.append_row(Data)
            st.success(f"Data Submitted Sucessfully and The ID is:{Id}")
            id_param = urllib.parse.quote(Id)
            amount_param = urllib.parse.quote(duplicate_amount)
            month_param = urllib.parse.quote(month)
            class_param = urllib.parse.quote(student_class)
            owner_param = urllib.parse.quote(author)
            redirect_url = f"/invoice?id={id_param}&duplicate_amount={amount_param}&month={month_param}&class={class_param}&author={owner_param}"
            st.markdown(f"""
            <meta http-equiv="refresh" content="0; url={redirect_url}">
            """, unsafe_allow_html=True)
        else:
            st.error("Please Enter The Data Perfectly")
    else:
        st.error("Admin Password Is Not Correct!")