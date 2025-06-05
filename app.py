import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yagmail
import random
from fpdf import FPDF
from io import BytesIO



scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

#creds = ServiceAccountCredentials.from_json_keyfile_name(
 #   r"C:\MIT_regestration form\demopythonsheet-462010-8bcba9d1911a.json", scope)

import os
cred_path = st.secrets["gspread"]["cred_path"]
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)


client = gspread.authorize(creds)
sheet_url = "https://docs.google.com/spreadsheets/d/1xY6RLbn__y3T7gnTJ7tCCDpbLbNYNsjidpDIhEiRn3w/edit?usp=sharing"
sheet = client.open_by_url(sheet_url).sheet1


def generate_unique_id():
    return "MIT" + ''.join([str(random.randint(0, 9)) for _ in range(3)])

def send_email(receiver_email, unique_id, name):
    #sender_email = "a15767089@gmail.com"
    #sender_password = "mmld ufkk xntg ucrt"

    sender_email = st.secrets["email"]["sender"]
    sender_password = st.secrets["email"]["password"]


    subject = "MIT Registration Successful"
    body = f"Dear {name},\n\nThank you for registering at MIT.\nYour Unique ID is: {unique_id}\n\nRegards,\nMIT Admissions"

    try:
        yag = yagmail.SMTP(user=sender_email, password=sender_password)
        yag.send(to=receiver_email, subject=subject, contents=body)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)


    def header(title):
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, title, ln=True, fill=True)

    def line_gap(h=5):
        pdf.ln(h)

    def draw_field(label, value, h=8):
        if value:  
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(60, h, f"{label}:", border=0)
            pdf.set_font("Arial", '', 10)
            pdf.cell(0, h, str(value), ln=True)

    def draw_double_field(label1, value1, label2, value2, h=8):
        if value1 or value2:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(45, h, f"{label1}:", border=0)
            pdf.set_font("Arial", '', 10)
            pdf.cell(50, h, str(value1), border=0)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(45, h, f"{label2}:", border=0)
            pdf.set_font("Arial", '', 10)
            pdf.cell(0, h, str(value2), ln=True)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "MEERUT INSTITUTE OF TECHNOLOGY", ln=True, align="C")
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "STUDENT REGISTRATION FORM", ln=True, align="C")
    pdf.ln(5)

    header("1. Personal Information")
    draw_field("Unique ID", data["Unique ID"])
    draw_double_field("Name", data["Name"], "Gender", data["Gender"])
    draw_double_field("Email", data["Email"], "Phone", data["Phone"])
    draw_field("Date of Birth", data["Date of Birth"])
    draw_field("Address", data["Address"])

    line_gap()
    header("2. Academic Information")
    draw_field("Course Applied For", data["Course"])
    draw_double_field("Entrance Exam Appeared", data["Appeared Entrance Exam"], "Exam Name", data["Entrance Exam Name"])
    draw_double_field("10th Percentage", f"{data['10th Percentage']}%", "12th Percentage", f"{data['12th Percentage']}%")

    line_gap(10)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, "Date: ____ / ____ / ______", ln=True)
    line_gap(5)
    pdf.cell(0, 10, "Candidate Signature: ___________________________", ln=True)
    line_gap(10)

    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "This is a computer-generated document. No signature required.", ln=True, align="C")

    pdf_output = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_output)



st.set_page_config(page_title="MIT Admission Form", layout="centered")

with st.spinner("Loading form..."):
    import time
    time.sleep(1.5)  

st.markdown("""
    <style>
        /* Animated Gradient Background */
        body {
            background: linear-gradient(270deg, #002855, #004080, #0059b3, #002855);
            background-size: 800% 800%;
            animation: gradientMove 20s ease infinite;
        }

        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
        }

        .stApp {
            max-width: 900px;
            margin: 0 auto;
            background-color: #ffffffdd;
            padding: 40px 30px 30px 30px;
            border-radius: 12px;
            box-shadow: 0px 0px 12px rgba(0,0,0,0.15);
        }

        h1, h4 {
            text-align: center;
            color: #ffffff;
            text-shadow: 1px 1px 2px #00000070;
        }

        .section-title {
            font-size: 20px;
            margin-top: 30px;
            font-weight: bold;
            color: #002855;
            border-bottom: 2px solid #00285520;
            padding-bottom: 6px;
        }

        .stTextInput > label, .stTextArea > label, .stSelectbox > label, .stRadio > label, .stNumberInput > label {
            font-weight: 600;
            color: #333333;
        }

        .stDownloadButton > button {
            background-color: #002855;
            color: white;
            font-weight: 600;
            padding: 8px 20px;
            border-radius: 6px;
        }

        .stDownloadButton > button:hover {
            background-color: #014aad;
            color: white;
        }

        .stFormSubmitButton > button {
            background-color: #004080;
            color: white;
            font-weight: bold;
            padding: 10px 25px;
            border-radius: 8px;
        }

        .stFormSubmitButton > button:hover {
            background-color: #0059b3;
        }

        .animate-fade {
            animation: fadeIn 1.2s ease-in-out both;
        }

        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="animate-fade">', unsafe_allow_html=True)

st.markdown("<h1>Meerut Institute of Technology</h1>", unsafe_allow_html=True)
st.markdown("<h4>Online Admission Registration Form</h4>", unsafe_allow_html=True)

with st.form("registration_form"):
    st.markdown('<div class="section-title">Personal Details</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
    with col2:
        gender = st.radio("Gender", ["Male", "Female", "Other"])
        dob = st.date_input("Date of Birth")
        address = st.text_area("Address")

    st.markdown('<div class="section-title">Academic Details</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        course = st.selectbox("Select Course", [
            "B.Tech CSE", "B.Tech ECE", "B.Tech ME", "BCA", "BBA",
            "B.Pharm", "D.Pharm", "B.Sc. Agri", "B.Com (H)"
        ])
        entrance = st.radio("Appeared for Entrance Exam?", ["Yes", "No"])
    with col4:
        entrance_name = st.text_input("Entrance Exam Name (if any)")
        tenth = st.number_input("10th Percentage", 0.0, 100.0)
        twelfth = st.number_input("12th Percentage", 0.0, 100.0)

    st.markdown('<br>', unsafe_allow_html=True)
    submitted = st.form_submit_button("Submit Application")

if submitted:
    if not name or not email:
        st.error("Please fill in at least Name and Email.")
    else:
        unique_id = generate_unique_id()

        row = [
            unique_id, name, email, phone, gender, str(dob),
            address if address else "",
            course, entrance,
            entrance_name if entrance_name else "",
            tenth, twelfth
        ]

        sheet.append_row(row, value_input_option='USER_ENTERED', table_range='A1')
        email_status = send_email(email, unique_id, name)

        data_dict = {
            "Unique ID": unique_id,
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Gender": gender,
            "Date of Birth": dob,
            "Address": address,
            "Course": course,
            "Appeared Entrance Exam": entrance,
            "Entrance Exam Name": entrance_name,
            "10th Percentage": tenth,
            "12th Percentage": twelfth
        }

        pdf_buffer = create_pdf(data_dict)

        st.success("Registration Successful!")

        with st.expander("View your registration summary"):
            st.markdown(f"""
                **Unique ID**: `{unique_id}`  
                **Email Sent**: `{email}` {"✅" if email_status else "❌"}  
                Download your registration PDF below:
            """)
            st.download_button(
                label="Download Registration PDF",
                data=pdf_buffer,
                file_name=f"{unique_id}_registration.pdf",
                mime="application/pdf"
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        


