import streamlit as st
import re
import sqlite3 as sq
from PIL import Image
import io
st.title("DATA ENTRY ")
st.header("WELCOME TO DATA ENTRY PAGE")
def main():
    # Collect user inputs using Streamlit widgets
    name = st.text_input('Enter Your name')

    email = st.text_input("Email")
    validate_email(email)

    mobile_number = st.text_input('Enter your mobile number (10 digits)', '')
    validate_mobile_number(mobile_number)

    dev_name = st.text_input('Enter the device name', key='input1')

    dev_loc = st.selectbox(label="Choose the device Found Location",
                           options=('Mangamuru Road', 'QIS COLLEGE', 'NG Road', 'Bus stand', 'Railway Station'))

    dev_adrs = st.text_area(label="Write the Full Address ", height=200, placeholder="write here")

    pin_code = st.text_input('Enter your pin code (6 digits)', '')
    validate_pin_code(pin_code)

    town_name = st.text_input('Enter the Town/Village Name', key='input2')

    selected_date = st.date_input("Select a date below:")

    selected_time = st.time_input("Select a time below:")

    uploaded_image = st.file_uploader("Upload an image below:", type=["jpg", "png", "jpeg"])
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    if st.button("Submit"):
        # Call the add function to insert data into the database
        add(name, email, mobile_number, dev_name, dev_loc, dev_adrs, pin_code, town_name, selected_date, selected_time,
            uploaded_image)


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


def validate_pin_code(pin_code):
    pattern = r"^\d{6}$"
    if re.match(pattern, pin_code):
        st.success(f'Valid pin code entered: {pin_code}')
    elif pin_code != "":
        st.error('Invalid pin code format. Please enter a 6-digit pin code.')


def add(name, email, mobile_number, dev_name, dev_loc, dev_adrs, pin_code, town_name, selected_date, selected_time,
        uploaded_image):
    connection = sq.connect("ENTRY.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ENTRY (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            mobile_number TEXT,
            dev_name TEXT,
            dev_loc TEXT,
            dev_adrs TEXT,
            dev_pin TEXT,
            dev_town TEXT,
            date TEXT,
            time TEXT,
            image_file BLOB
        )
    ''')

    cursor.execute('''
        INSERT INTO ENTRY (
            name,
            email,
            mobile_number,
            dev_name,
            dev_loc,
            dev_adrs,
            dev_pin,
            dev_town,
            date,
            time,
            image_file
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, mobile_number, dev_name, dev_loc, dev_adrs, pin_code, town_name,
          str(selected_date), str(selected_time), uploaded_image.read() if uploaded_image else None))
    cursor.execute("SELECT * FROM ENTRY WHERE name = ?", (name,))
    data = cursor.fetchall()
    if data:
        # Display data as a table using st.table
        st.table(data)

        # Alternatively, you can display data as a dataframe using st.dataframe
        # import pandas as pd
        # df = pd.DataFrame(data, columns=["Column1", "Column2", ...])
        # st.dataframe(df)
        # Display images
        for row in data:
            image_data = row[-1]  # Assuming the last column contains image data
            if image_data:
                image = Image.open(io.BytesIO(image_data))
                st.image(image, caption="Image", use_column_width=True)
            else:
                st.write("No image available for this row.")
    else:
        st.write("No data found in the table.")

        # Close the database connection
    # Commit changes and close connection
    connection.commit()
    connection.close()


main()
