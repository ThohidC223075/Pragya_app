import streamlit as st
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from google.auth.exceptions import TransportError
from gspread_client import client
st.set_page_config(layout="wide")

query_params = st.query_params
teacher_id = query_params.get("teacher_id", None)
selected_date = query_params.get("selected_date", None)

if teacher_id and selected_date:
    try:
        selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        st.error("Invalid date format in URL.")
else:
    st.warning("No teacher ID or date provided in the URL.")

# Google Sheets setup
#scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)

#sheet2 = client.open("Coaching_Management").worksheet("Teacher_Taken_Class_Information")
#sheet1 = client.open("Coaching_Management").worksheet("Teacher_Information")
#sheet3 = client.open("Coaching_Management").worksheet("Teacher_Class_Wise_Salary")

try:
    sheet2 = client.open("Coaching_Management").worksheet("Teacher_Taken_Class_Information")
    sheet1 = client.open("Coaching_Management").worksheet("Teacher_Information")
    sheet3 = client.open("Coaching_Management").worksheet("Teacher_Class_Wise_Salary")
except TransportError as e:
    st.error("🔌 Network error! Could not connect to Google services. Please check your internet connection and try again.")
    st.stop()
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {e}")
    st.stop()











data3 = sheet3.get_all_records()
df3 = pd.DataFrame(data3)

data = sheet2.get_all_records()
df = pd.DataFrame(data)

data1 = sheet1.get_all_records()
df1 = pd.DataFrame(data1)
result = df1[df1['ID'] == teacher_id][['Name', 'Phone']]

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')

# Design
col1, col2, col3 = st.columns([1, .35, 1])
with col2:
    st.image("images/pragya.jpeg", width=120)

main_font = "Times New Roman"
content_font = "Bell MT"
green_color = "#00695C"

st.markdown(f"""
    <div style='text-align: center; padding: 10px;margin-top:-25px; font-family: {main_font};'>
        <h1 style='color: {green_color}; margin-bottom: 5px;'>PRAGYA ACADEMIC CARE</h1>
        <p style='color: black; font-size: 20px;margin-top:-15px;'>
            Address: Khaza Road, Aminer Dokan<br>
            Phone: 01517109771
        </p>
        <h2 style='color: {green_color}; margin-top:-20px;margin-left:20px;'>SALARY</h2>
    </div>
""", unsafe_allow_html=True)

# Custom CSS
st.markdown(f"""
<style>
.page-content {{
    padding: 0 40px;
    font-family: {content_font};
}}
.info-box {{
    padding: 10px;
    border-radius: 6px;
    background-color: #f1f1f1;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
    margin-top: 5px;
    font-family: {content_font};
}}
.label {{
    font-weight: bold;
    margin-bottom: 3px;
    font-family: {content_font};
}}
.dataframe-wrapper {{
    padding: 20px;
    margin-top: 20px;
    text-align: center;
}}
thead tr th, tbody tr td {{
    text-align: center !important;
    vertical-align: middle !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='page-content'>", unsafe_allow_html=True)

# Info box
def student_info_row(label1, value1, label2=None, value2=None):
    if label2 and value2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='label'>{label1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'>{value1}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='label'>{label2}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'>{value2}</div>", unsafe_allow_html=True)
    else:
        col1, _ = st.columns([1, 1])
        with col1:
            st.markdown(f"<div class='label'>{label1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'>{value1}</div>", unsafe_allow_html=True)

if not result.empty:
    name = result['Name'].iloc[0]
    phone = result['Phone'].iloc[0]
    student_info_row("Name:", name, "Teacher ID:", teacher_id)
    student_info_row("Date:", selected_date, "Phone:", phone)
else:
    st.error("Teacher not found. Please check ID.")

if teacher_id and selected_date:
    selected_date_dt = pd.to_datetime(selected_date)
    filtered_df = df[
        (df['ID'] == teacher_id) &
        (df['Date'] <= selected_date_dt) &
        (df['Paid'] == "No")
    ]

    if not filtered_df.empty:
        filtered_df = filtered_df.drop(columns=['ID', 'Date', 'Paid'])
        filtered_df = filtered_df.apply(pd.to_numeric, errors='coerce')

        classes = ['6', '7', '8', '9', '10', '11', '12']
        row = pd.DataFrame(df3.loc[df3['ID'] == teacher_id])
        row = row.drop(columns=['ID'])

        output_df = pd.DataFrame(columns=['Class', 'Total Class', 'Amount (Per Class)', 'Total'])

        subtotal = 0
        for class_name in classes:
            total_class_value = filtered_df[f'Class-{class_name}'].sum()
            amount_per_class = row.iloc[0][f'Amount-{class_name}']
            total_value = total_class_value * amount_per_class
            subtotal += total_value
            new_row = {
                'Class': class_name,
                'Total Class': total_class_value,
                'Amount (Per Class)': amount_per_class,
                'Total': total_value
            }
            output_df = pd.concat([output_df, pd.DataFrame([new_row])], ignore_index=True)

        df = output_df.reset_index(drop=True)
#html_table = df.to_html(index=False, escape=False)
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
        # Subtotal
        st.markdown(f"<p style='font-size:20px;margin-top:5px; font-weight:bold;'>Subtotal: {subtotal}</p>", unsafe_allow_html=True)
    else:
        st.warning("No unpaid data found for this teacher before the selected date.")
else:
    st.error("Please enter both Teacher ID and Date.")

# Final notes
st.markdown(f"""
<div style='text-align: left; color: black; margin-top:5px; font-size: 20px; font-family: {content_font};'>
    <b>Very Grateful to you for being a member of our Pragya family with obedience.</b><br>
    May you be a Pearl of Pragya in your lifeline so far..
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    st.markdown(f"<p style='color: black;font-size:20px;margin-top:0px;font-family:{content_font};'><b>Powered by</b></p>", unsafe_allow_html=True)
    st.image("images/codetroon.jpg", width=100)

data = sheet2.get_all_values()
rows = data[1:]
delete_count = 0
for i in reversed(range(len(rows))):
    row = rows[i]
    row_id = row[0]
    row_date_str = row[1]
    try:
        row_date = datetime.datetime.strptime(row_date_str, '%Y-%m-%d').date()
    except ValueError:
        continue
    if row_id == teacher_id and row_date <= selected_date:
        sheet2.delete_rows(i + 2) 
        delete_count += 1
#if delete_count:
    #st.success(f"{delete_count} row(s) deleted.")
else:
    st.warning("No matching rows found.")