import streamlit as st

class HomePage:
    def __init__(self):
        self.title = "Criminal Detection and Report"
        self.logo_path = "logo.png"
        self.tagline = "Revolutionizing Justice with Face Recognition"
        self.explanation = "The cutting-edge Criminal Report Application that harnesses advanced face recognition technology to detect and report criminals. Explore the future of crime prevention through our modern interface, where you can effortlessly view criminal profiles, add new records, and unlock a world of possibilities. Join us in shaping a safer tomorrow with the seamless synergy of technology and justice."
        self.how_to_use = "To use the application, follow these steps:\n1. Click on 'Criminal List' to view criminal profile\n1. Click on 'Detection' to detect criminal.\n2. Click on 'Report' to add a new records."
        self.terms_and_conditions = "By using this application, you agree to abide by the terms and conditions outlined in the Criminal Report Application's policy."

    def display(self):
        st.markdown(f"<h1 style='text-align: center; margin-bottom: 1em;'>{self.title}</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.write("")

        with col2:
            st.image(self.logo_path, use_column_width=True)

        with col3:
            st.write("")

        st.markdown(f"<h3 style='text-align: center; margin-top: 1em; margin-bottom: 2em;'>{self.tagline}</h3>", unsafe_allow_html=True)

        st.markdown("### Welcome to the Apps!")
        st.write(self.explanation)

        st.markdown("### How to Use")
        st.write(self.how_to_use)

        st.markdown("### Terms and Conditions")
        st.write(self.terms_and_conditions)