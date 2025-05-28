import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime
from google.auth.exceptions import TransportError
from gspread_client import client


st.set_page_config(page_title="Insert Data", layout="wide")
st.title("Insert Coaching Cost")

# Step 1: Auth and connect
#scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)
#sheet = client.open("Coaching_Management").worksheet("Coaching_Cost")

try:
    sheet = client.open("Coaching_Management").worksheet("Coaching_Cost")
except TransportError as e:
    st.error("🔌 Network error! Could not connect to Google services. Please check your internet connection and try again.")
    st.stop()
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {e}")
    st.stop()
# -------------------- INSERT SECTION --------------------
# First Row
col1, col2 = st.columns(2)
with col1:
    selected_date = str(st.date_input("Select Date", datetime.date.today()))
with col2:
    reason = st.text_input("Reason")

# Second Row
col3, col4 = st.columns(2)
with col3:
    amount = st.text_input("Amount")
with col4:
    password = st.text_input("Admin Password",type="password")

#Accessing the password
my_password = st.secrets["password"]



if st.button("Submit"):
    if selected_date.strip() and reason.strip() and amount.strip() and password == my_password:
        data = [selected_date, reason, amount]
        sheet.append_row(data)
        st.success("Data Submitted Successfully")
    elif password!=my_password:
        st.error("Admin Password is not Correct")
    else:
        st.error("Please Insert Correct Information")

# -------------------- FETCH SECTION --------------------
st.title("See Coaching Cost Using Date")

col1, col2 = st.columns(2)
with col1:
    starting_date = str(st.date_input("Select Start Date", datetime.date.today()))
with col2:
    ending_date = str(st.date_input("Select End Date", datetime.date.today()))

col3, col4 = st.columns(2)
with col3:
    fetch_password = st.text_input("Admin Password", key="fetch",type="password")


if st.button("Fetch"):
    if starting_date.strip() and ending_date.strip() and fetch_password == my_password:
        # Convert start and end dates to datetime64[ns] for correct comparison
        starting_date = pd.to_datetime(starting_date)
        ending_date = pd.to_datetime(ending_date)

        # Load data from sheet
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        # Parse 'Date' column as datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')

        # Filter rows within date range
        filtered_df = df[(df['Date'] >= starting_date) & (df['Date'] <= ending_date)]
        filtered_df['Date'] = filtered_df['Date'].dt.date
        total_amount = filtered_df['Amount'].sum()

        # Display results
        #st.dataframe(filtered_df)
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
        st.table(filtered_df) 
        st.write(f"Total Cost: {total_amount}")
    elif password!=my_password:
        st.error("Admin Password is not Correct")
    else:
        st.error("Please Insert Correct Information")
