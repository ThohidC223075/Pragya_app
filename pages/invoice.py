import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from google.auth.exceptions import TransportError
from gspread_client import client
# Step 1: Auth and connect
#scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
#client = gspread.authorize(creds)

# --- Page Config ---
st.set_page_config(page_title="Invoice", layout="wide")

def find_row_by_id(sheet, target_id):
    records = sheet.get_all_records()
    for index, row in enumerate(records):
        if str(row["ID"]) == str(target_id):
            return index + 2  # +2 because of header row and 1-indexing
    return None

# Get query parameters
query_params = st.query_params
id = query_params.get("id", "")
amount = query_params.get("duplicate_amount", "")
month = query_params.get("month", "")
student_class = query_params.get("class", "")
author = query_params.get("author", "")

# Declare values
name = ""
g_name = ""
phone = ""
institute = ""
group = ""
current_date = datetime.today().date()

# Load Google Sheet
try:
    sheet_name = "Student_Information_Class" + student_class
    sheet = client.open("Coaching_Management").worksheet(sheet_name)
except TransportError as e:
    st.error("🔌 Network error! Could not connect to Google services. Please check your internet connection and try again.")
    st.stop()
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {e}")
    st.write("You Can't Access The Invoice Page Directly. At first go to Student Payment")
    st.stop()
#sheet_name = "Student_Information_Class" + student_class
#sheet = client.open("Coaching_Management").worksheet(sheet_name)
row_num = find_row_by_id(sheet, id)

if row_num:
    headers = sheet.row_values(1)
    row_data = sheet.row_values(row_num)
    row_dict = dict(zip(headers, row_data))
    name = row_dict.get("Name", "")
    g_name = row_dict.get("Guardian Name", "")
    phone = row_dict.get("Phone", "")
    institute = row_dict.get("Institute", "")
    group = row_dict.get("Group", "")
else:
    st.error("Id not found")

# Logo
col1, col2, col3 = st.columns([1, .45, 1])
with col2:
    #st.image("images/pragya.jpeg", width=120)
    #st.image("../images/pragya.jpeg", width=120)
    st.image("pragya.jpeg", width=120)


# --- Custom Colors and Fonts ---
primary_color = "#00695C"
title_font = "Times New Roman"
body_font = "Bell MT"

# --- Coaching Info ---
st.markdown(f"""
    <div style='text-align: center; padding: 10px; margin-top:-25px; font-family: "{title_font}";'>
        <h1 style='color: {primary_color}; margin-bottom: 5px;'>PRAGYA ACADEMIC CARE</h1>
        <p style='color: black; font-size: 20px; margin-top:-15px;'>
            Address: Khaza Road, Aminer Dokan<br>
            Phone: 01517109771
        </p>
        <div style='
            display: inline-block;
            padding: 4px 10px;
            border: 1px solid {primary_color};
            border-radius: 4px;
            background-color: #E0F2F1;
            color: {primary_color};
            font-size: 28px;
            font-weight: bold;
            margin-top: -10px;
        '>
            INVOICE
        </div>
    </div>
""", unsafe_allow_html=True)


# --- Custom CSS for Content Area ---
st.markdown(f"""
<style>

.info-box {{
    padding: 10px;
    border-radius: 6px;
    background-color: #f1f1f1;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
    margin-top: 5px;
    font-family: "{body_font}";
}}
.label {{
    font-weight: bold;
    margin-bottom: 3px;
    font-family: "{body_font}";
}}
</style>
""", unsafe_allow_html=True)

# --- Page Wrapper Start ---
#st.markdown("<div class='page-content'>", unsafe_allow_html=True)

# --- Info Row Helper ---
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

# --- Student Info Display ---
student_info_row("Name:", name, "Student ID:", id)
student_info_row("Amount:", amount, "Class:", student_class)
student_info_row("Phone:", phone, "Month:", month)
student_info_row("Issue Date:", current_date, "Institute:", institute)
student_info_row("Received By:", author, "Group", group)
#student_info_row("Amount:", amount)

# --- Appreciation Note ---
st.markdown(f"""
<div style='text-align: center; color: black; margin-top: 25px; font-size: 20px; font-family: "{body_font}";'>
    <b>Very Grateful to you for being a member of our Pragya family with obedience.</b><br>
    May you be a Pearl of Pragya in your lifeline so far..
</div>
""", unsafe_allow_html=True)

# --- Page Wrapper End ---
st.markdown("</div>", unsafe_allow_html=True)

# --- Footer Section ---
#col1, col2, col3 = st.columns([3, 1, 1])
#with col3:
    #st.markdown(f"<p style='color: black; font-size: 20px; margin-top: -10px; font-family: \"{body_font}\";'><b>Powered by</b></p>", unsafe_allow_html=True)
    #st.image("codetroon.jpg", width=100)

col1, col2, col3 = st.columns([3, 1, 2])  # Adjust proportions as needed

with col3:
    text_col, image_col = st.columns([1, 1])  # Side by side in col3
    with text_col:
        st.markdown(
            f"<p style='color: black; font-size: 25px; margin-top: 5px; font-family: \"{body_font}\";'><b>Powered by</b></p>",
            unsafe_allow_html=True
        )
    with image_col:
        st.image("codetroon.jpg", width=110)  # Make sure the image file exists in the right location
