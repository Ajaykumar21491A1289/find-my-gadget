import streamlit as st
import re
import sqlite3 as sq
from PIL import Image
import io
st.title("WELCOME TO DATA DELETING PAGE")
def main():
    name = st.text_input('Enter Your name')
    email = st.text_input("Email")
    validate_email(email)
    mobile_number = st.text_input('Enter your mobile number (10 digits)', '')
    validate_mobile_number(mobile_number)
    dev_name = st.text_input('Enter the device name', key='input1')
    if st.button("Submit"):
        # Call the add function to insert data into the database
        delete(name, email, mobile_number, dev_name)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        st.success("Valid email address!")
    elif email != "":
        st.error("Invalid email address. Please enter a valid email.")
def validate_mobile_number(mobile_number):
    pattern = r"^\d{10}$"
    if re.match(pattern, mobile_number):
        st.success(f'Valid mobile number entered: {mobile_number}')
    elif mobile_number != "":
        st.error('Invalid mobile number format. Please enter a 10-digit number.')


def delete(name, email, mobile_number, dev_name):
     connection = sq.connect("../pages/ENTRY.db")
     cursor = connection.cursor()
     cursor.execute("DELETE * FROM ENTRY WHERE name=? or email =? or mobile_number=? or dev_name=? ", (name,email,mobile_number,dev_name))
main()