import streamlit as st

class CriminalList:
    def __init__(self):
        self.criminals = []

    def add_criminal(self, name, age, sex, height, weight, description, photo, details):
        self.criminals.append({
            'Name': name,
            'Age': age,
            'Sex': sex,
            'Description': description,
            'Photo': photo,
            'Height': height,
            'Weight': weight,
            'Details': details
        })

    def display(self):
        st.markdown("<h1 style='text-align: center; margin-bottom: 1em;'>List of Criminals</h1>", unsafe_allow_html=True)
        if len(self.criminals) == 0:
            st.write("No criminals found.")
        else:
            num_columns = 2
            num_criminals = len(self.criminals)
            num_rows = (num_criminals + num_columns - 1) // num_columns

            cols = st.columns(num_columns)

            for index, criminal in enumerate(self.criminals):
                col_index = index % num_columns
                row_index = index // num_columns
                with cols[col_index]:
                    st.subheader(f"Criminal {index + 1}")
                    st.write("Name:", criminal['Name'])
                    st.write("Description:", criminal['Description'])
                    st.image(criminal['Photo'], caption='Criminal Photo', use_column_width=True)
                    button_key = f"details_button_{index}"
                    if st.button("View Details", key=button_key):
                        self.display_criminal_details(criminal)
                    st.write("---")

    @staticmethod
    def display_criminal_details(criminal):
        st.subheader(f"Criminal Details:")
        st.write("Name:", criminal['Name'])
        st.write(f"Sex: {criminal['Sex']}")
        st.write(f"Age: {criminal['Age']}")
        st.write(f"Height: {criminal['Height']} cm")
        st.write(f"Weight: {criminal['Weight']} kg")
        st.write("Description:", criminal['Description'])
        st.write("Details:", criminal['Details'])