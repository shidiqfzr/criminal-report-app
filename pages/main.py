import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st
from streamlit_option_menu import option_menu
from home import HomePage
from criminalList import CriminalList
from detection import CriminalDetector
from report import CriminalReporter

hide_st_style = """ 
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True) # hide streamlit menu

# --- USER AUTHENTICATION ---
with open('pages/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# authentication_status = None
    
name, authentication_status, username = authenticator.login('Login', 'main')

class MainMenu:
    def run(self):
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",
                options=["Home", "Criminal List", "Detection", "Report", "Logout"],
                icons=["house", "person-lines-fill", "camera", "flag", "box-arrow-left"],
                menu_icon="cast",
                default_index=0
            )

        if selected == "Home":
            homepage = HomePage()
            homepage.display()
        
        elif selected == "Criminal List":
            criminal_list = CriminalList()
            
            criminal_list.add_criminal(
                name="Achmad Shidiq",
                sex='Male',
                age=20,
                description="Robbery",
                height=167,
                weight=50,
                photo='CriminalImages/Achmad Shidiq.jpg',
                details="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac ultrices metus. Mauris consectetur nunc id libero posuere, eget efficitur ligula viverra. Suspendisse potenti. Sed sed quam vel odio varius auctor."
            )
            criminal_list.add_criminal(
                name="John Doe",
                sex='Male',
                age=35,
                description="Assault",
                height=180,
                weight=70,
                photo='CriminalImages/Carlos Ramirez.jpg',
                details="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac ultrices metus. Mauris consectetur nunc id libero posuere, eget efficitur ligula viverra. Suspendisse potenti. Sed sed quam vel odio varius auctor."
            )
            criminal_list.add_criminal(
                name="Emma Davis",
                sex='Female',
                age=35,
                description="Robbery",
                height=160,
                weight=60,
                photo='CriminalImages/Emma Davis.jpg',
                details="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac ultrices metus. Mauris consectetur nunc id libero posuere, eget efficitur ligula viverra. Suspendisse potenti. Sed sed quam vel odio varius auctor."
            )
            criminal_list.add_criminal(
                name="John Anderson",
                sex='Male',
                age=35,
                description="Robbery",
                height=180,
                weight=70,
                photo='CriminalImages/John Anderson.jpg',
                details="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac ultrices metus. Mauris consectetur nunc id libero posuere, eget efficitur ligula viverra. Suspendisse potenti. Sed sed quam vel odio varius auctor."
            )
            criminal_list.add_criminal(
                name="Robert Johson",
                sex='Male',
                age=32,
                description="Assault",
                height=174,
                weight=60,
                photo='CriminalImages/Robert Johson.jpg',
                details="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac ultrices metus. Mauris consectetur nunc id libero posuere, eget efficitur ligula viverra. Suspendisse potenti. Sed sed quam vel odio varius auctor."
            )
            criminal_list.add_criminal(
                name="Samantha Thompson",
                sex='Female',
                age=35,
                description="Fraud",
                height=165,
                weight=54,
                photo='CriminalImages/Samantha Thompson.jpg',
                details="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac ultrices metus. Mauris consectetur nunc id libero posuere, eget efficitur ligula viverra. Suspendisse potenti. Sed sed quam vel odio varius auctor."
            )

            criminal_list.display()

        elif selected == "Detection":
            path = 'CriminalImages'
            detector = CriminalDetector(path)
            st.markdown("<h1 style='text-align: center; margin-bottom: 1em;'>Criminal Detection</h1>", unsafe_allow_html=True)
            st.write("Initializing the criminal detection system...")
            st.write("Please grant permission to access the camera")
            run_camera = st.checkbox("Run Camera", key='run_camera')

            if run_camera:
                detector.detect_criminals()
            else:
                st.write("Camera is not running")

        elif selected == "Report":
            reporter = CriminalReporter()
            reporter.run()
        
        elif  selected == "Logout":
            st.warning("Are you sure want to exit?")
            authenticator.logout("Logout")


if __name__ == "__main__":
    if authentication_status is False:
        st.error("Username/password is incorrect")

    if authentication_status is None:
        st.warning("Please enter your username and password")
    
    if authentication_status:
        st.sidebar.markdown(
            f"<p style='font-size: 18px; font-weight: bold; margin-top: 10px; margin-bottom: 20px;'>Welcome {name}</p>",
            unsafe_allow_html=True
        )
        menu = MainMenu()
        menu.run()