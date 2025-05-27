import streamlit as st
import datetime
import urllib.parse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from google.auth.exceptions import TransportError
from gspread_client import client

# Step 1: Auth and connect
#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)
sheet_name="Teacher_Taken_Class_Information"
sheet=client.open("Coaching_Management").worksheet(sheet_name)



try:
    sheet_name="Teacher_Taken_Class_Information"
    sheet=client.open("Coaching_Management").worksheet(sheet_name)
    sheet_name="Teacher_Information"
    sheet1 = client.open("Coaching_Management").worksheet(sheet_name)
except TransportError as e:
    st.error("🔌 Network error! Could not connect to Google services. Please check your internet connection and try again.")
    st.stop()
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {e}")
    st.stop()





# Step 2: Get all data and load into a DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Step 3: Convert string date to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')


st.set_page_config(layout="wide")
st.title("Teacher Information Lookup")

# Input Section
st.subheader("Search Teacher")

col1, col2 = st.columns(2)
with col1:
    teacher_id = st.text_input("Enter Teacher ID")
with col2:
    selected_date = st.date_input("Select Date", datetime.date.today())

st.write("(If You Want to See Individual Information Then Fill The Teacher ID & Date Otherwise Don't Do Anything)")
col3, col4 = st.columns(2)
with col3:
    option = st.selectbox(
    "Select your class:",
    ["Individual","All"]
   )


# Submit Button
if st.button("Submit"):
    if option == "Individual":
        if teacher_id and selected_date:
            selected_date_dt = pd.to_datetime(selected_date)

            # Filter logic
            filtered_df = df[
                (df['ID'] == teacher_id) &
                (df['Date'] <= selected_date_dt) &
                (df['Paid'] == "No")
            ]

            if not filtered_df.empty:
                st.success("Unpaid records found:")
                #st.dataframe(filtered_df)
                df = pd.DataFrame(filtered_df)
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
            else:
                st.warning("No unpaid data found for this teacher before the selected date.")
        else:
            st.error("Please enter both Teacher ID and Date.")
         
    elif option=="All":
        data = sheet1.get_all_records()
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

if st.button("Paid"):
    teacher_id_param = urllib.parse.quote(teacher_id)
    selected_date_param = urllib.parse.quote(selected_date.strftime('%Y-%m-%d'))
    
    redirect_url = f"/teacher_salary?teacher_id={teacher_id_param}&selected_date={selected_date_param}"
    
    st.markdown(f"""
    <meta http-equiv="refresh" content="0; url={redirect_url}">
    """, unsafe_allow_html=True)