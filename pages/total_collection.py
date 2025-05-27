import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime
from gspread_client import client
# Step 1: Auth and connect
#scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)

st.set_page_config(page_title="Insert Data", layout="wide")
st.title("See Total Collection")

# -------------------- INSERT SECTION --------------------
# First Row
col1, col2 = st.columns(2)
with col1:
    starting_date = str(st.date_input("Starting Date", datetime.date.today()))
with col2:
    ending_date = str(st.date_input("Ending Date", datetime.date.today()))

# Second Row
col3, col4 = st.columns(2)
with col3:
    student_class = st.selectbox(
        "Class:",
        ["6", "7", "8", "9", "10", "11", "12"]
    )
with col4:
    option = st.selectbox(
        "Option:",
        ["Individual", "All"]
    )

# Accessing the Sheet
sheet_name = "Student_Salary_information_Class" + student_class
sheet = client.open("Coaching_Management").worksheet(sheet_name)

if starting_date.strip() and ending_date.strip() and student_class.strip() and option.strip():
    if st.button("Submit") and option == "Individual":
        # Convert start and end dates to datetime
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
        st.markdown("""
            <style>
                table { width: 100%; text-align: center !important; }
                th, td { text-align: center !important; }
            </style>
        """, unsafe_allow_html=True)

        st.table(filtered_df)
        st.write(f"Total Cost: {total_amount}")

    elif st.button("submit") and option == "All":
        starting_date = pd.to_datetime(starting_date)
        ending_date = pd.to_datetime(ending_date)
        class_list = ["6", "7", "8", "9", "10", "11", "12"]
        new_dataframe = pd.DataFrame(columns=['Class', 'Amount'])
        total_collection = 0

        for class_name in class_list:
            sheet_name = "Student_Salary_information_Class" + class_name
            sheet = client.open("Coaching_Management").worksheet(sheet_name)
            data = sheet.get_all_records()
            df = pd.DataFrame(data)

            if df.empty:
                total_amount = 0
            else:
                df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
                filtered_df = df[(df['Date'] >= starting_date) & (df['Date'] <= ending_date)]
                filtered_df['Date'] = filtered_df['Date'].dt.date
                total_amount = filtered_df['Amount'].sum()

            total_collection += total_amount
            new_row = pd.DataFrame([[class_name, total_amount]], columns=['Class', 'Amount'])
            new_dataframe = pd.concat([new_dataframe, new_row], ignore_index=True)

        # Display the final results
        st.markdown("""
            <style>
                table { width: 100%; text-align: center !important; }
                th, td { text-align: center !important; }
            </style>
        """, unsafe_allow_html=True)

        st.table(new_dataframe)
        st.write(f"Total Collection: {total_collection}")
else:
    st.error("Please Insert Correct Information")
