import streamlit as st
import os
import mysql.connector


class CriminalReporter:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Shubuh28Mei2003',
            database='criminal'
        )

    def __del__(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def convertToBinaryData(self, filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    def insertData(self, name, age, gender, date, location, crime_category, crime_desc, photo):
        print("Inserting data into table")
        try:
            cursor = self.connection.cursor()

            sql_insert_query = """
                INSERT INTO criminal_report (name, age, gender, date, location, crime_category, crime_desc, photo) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            crimePic = self.convertToBinaryData(photo)

            # Convert data into tuple format
            insert_tuple = (name, age, gender, date, location, crime_category, crime_desc, crimePic)
            cursor.execute(sql_insert_query, insert_tuple)
            self.connection.commit()
            print("Data inserted successfully")
            return True  # Indicate successful insertion

        except mysql.connector.Error as error:
            print("Failed to insert data into table: {}".format(error))
            return False  # Indicate failure

        finally:
            cursor.close()

    def save_uploaded_file(self, uploaded_file):
        file_path = os.path.join("CriminalImages", uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return file_path

    def run(self):
        st.markdown("<h1 style='text-align: center; margin-bottom: 1em;'>Criminal Report</h1>", unsafe_allow_html=True)
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female"])
        date = st.date_input("Date")
        location = st.text_input("Location")
        crime_category = st.selectbox("Crime Category", ["Theft", "Assault", "Fraud", "Other"])
        crime_desc = st.text_area("Crime Description")
        photo = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'])

        if st.button("Submit"):
            if name and age and gender and date and location and crime_category and crime_desc and photo:
                temp_file_path = self.save_uploaded_file(photo)
                if self.insertData(name, age, gender, date, location, crime_category, crime_desc, temp_file_path):
                    st.success("Data saved successfully!")
                else:
                    st.error("Failed to save data.")
            else:
                st.warning("Please fill in all the required fields.")