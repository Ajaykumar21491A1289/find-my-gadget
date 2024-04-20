import streamlit as st
import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
def login_page():
    def verify_user(username, password):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Retrieve the hashed password for the given username
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        conn.close()

        # If the username exists, verify the password
        if result:
            return pbkdf2_sha256.verify(password, result[0])

        return False

    def fun():
        import streamlit as st
        import sqlite3 as sq
        connection = sq.connect("mydatabase.db")
        cursor = connection.cursor()
        st.title("YOU HAVE LOGIN SUCCESSFULLY")

    st.title("LOGIN PAGE")
    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    login_button = st.button("Login")

    # Check login credentials
    if login_button:
        if verify_user(username, password):
            st.success("Login successful!")
            fun()
        else:
            st.error("Login failed. Please check your credentials.")

def register_page():


    def create_user_table():
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Create a user table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_user(username, password):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            # Hash the password before storing it
            hashed_password = pbkdf2_sha256.hash(password)

            # Insert user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))

            conn.commit()
            st.success("Registration successful!")
        except sqlite3.IntegrityError:
            # This exception is raised if the username already exists
            st.error("Username already exists. Please choose a different username.")
        finally:
            conn.close()
    return True
    st.title("REGISTER PAGE")

    create_user_table()

    # Sidebar for registration
    st.write("ENTER YOUR DETAILS")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    register_button = st.button("Register")

    # Register new user
    if register_button:
        add_user(new_username, new_password)

def main():
    st.set_page_config(
        page_title="Your App Title",
        page_icon=":shark:",
        initial_sidebar_state="expanded",
    )
    st.image("https://wallpapercave.com/wp/wp9764081.jpg")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Login", "Register"))

    if page == "Login":
        if login_page():
            # If login is successful, show the registration page
            register_page()
    elif page == "Register":
        register_page()


main()
