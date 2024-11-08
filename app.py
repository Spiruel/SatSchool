import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import time
import json

import streamlit as st
from st_pages import Page, show_pages, add_indentation, Section
import geemap
from pathlib import Path

import ee
# ee.Authenticate()
# ee.Initialize(project='ee-spiruel')
# geemap.ee_initialize(**{'project':'ee-spiruel'})

from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import time
import json

st.set_page_config(layout="wide", page_title="SatSchool", page_icon="🛰️")


st.session_state["warned_about_save_answers"] = True

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages(
    [
        Section(name="", icon="🏠"),
        Page("app.py", "Home", ""),
        Page("pages/intro/timeline.py", "Timeline", ""),
        Page("pages/intro/timelapse.py", "Timelapse", ""),
        Page("pages/intro/lights.py", "Night Lights", ""),
        Section(name=" ", icon="🌲"),
        Page("pages/land/classifier.py", "Deforestation", ""),
        Page("pages/land/juxtapose.py", "Compare", ""),
        Section(name="  ", icon="🌊"),
        Page("pages/oceans/sst_chla.py", "Sea Surface Temperature", ""),
        Section(name="   ", icon="🧊"),
        Page("pages/ice.py", "Ice", ""),
        Section(name="    ", icon=":books:"),
        Page("pages/quiz.py", "Quiz", ""),
    ]
)
add_indentation()

with st.sidebar:

    st.sidebar.title("About")
    st.sidebar.info(
        """
        🌐 https://eo-cdt.org
        
        ©️ 2024 SatSchool
    """
    )

logo = True

with open ('./pages/intro/satschoollottie.json', 'r') as f:
    lottie_satschool = json.load(f)
    
st.title('SatSchool - Hands on with Data')

a,b = st.columns([0.3,0.5])

with a:
    st_lottie(lottie_satschool, key="lottie_satschool", speed=0.5, loop=False, quality='high', width=400)
   
b.markdown("""Welcome to the 'Hands on with Data' module as part of SatSchool. 🚀🚀🚀

For the main SatSchool website, please visit **[https://satschool-outreach.github.io](https://satschool-outreach.github.io)**.



In this module you will learn how to manipulate and understand data from satellites in a range of environmental contexts. It's your chance to get hands on with satellite data!

You will learn:

* How scientists work with satellite data to better understand different parts of the Earth system
* How to work with different kinds of satellite data yourself and the types of information it contains
* How to interpret maps and graphs displaying different types of environmental data

<img src="https://www.gim-international.com/cache/a/f/b/3/2/afb32cbe5b80419c8de0d63398cfb5c661498273.jpeg" alt="Sentinel 2" width="700">""", unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
