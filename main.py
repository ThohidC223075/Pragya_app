import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #111111;  /* Dark black background */
        }
        .rectangle-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: space-between;
            padding: 20px;
        }
        .rectangle {
            background-color: #ff8c00;  /* Orange color for rectangles */
            width: 30%;
            min-width: 250px;
            height: 200px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: transform 0.2s;
            text-decoration: none !important;
            color: white !important;  /* White text color */
        }
        .rectangle:hover {
            transform: scale(1.03);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.45);
            background-color: #e07b00;  /* Darker orange on hover */
        }
        .rectangle h4 {
            margin: 0;
            text-align: center;
            text-decoration: none;
            font-size: 18px;
        }
        .rectangle:link,
        .rectangle:visited,
        .rectangle:hover,
        .rectangle:active {
            text-decoration: none;
            color: white;
        }
    </style>

    <div class="rectangle-container">
        <a href="/insert_student_data" target="_blank" class="rectangle">
            <h4>Insert Data(Student)</h4>
        </a>
        <a href="/update_student_data" target="_blank" class="rectangle">
            <h4>Update Data(Student)</h4>
        </a>
        <a href="/insert_teacher_data" target="_blank" class="rectangle">
            <h4>Insert Data(Teacher)</h4>
        </a>
        <a href="/update_teacher_data" target="_blank" class="rectangle">
            <h4>Update Data(Teacher)</h4>
        </a>
        <a href="/see_student_information" target="_blank" class="rectangle">
            <h4>Student Information</h4>
        </a>
        <a href="/see_teacher_information" target="_blank" class="rectangle">
            <h4>Teachers Information</h4>
        </a>
            <a href="/teacher_taken_class" target="_blank" class="rectangle">
            <h4>Teachers Class Attendance</h4>
        </a>
        <a href="/teacher_class_wise_salary" target="_blank" class="rectangle">
            <h4>Teacher Class Wise Salary Input</h4>
        </a>
    </div>
""", unsafe_allow_html=True)
