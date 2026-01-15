import streamlit as st
from registration import reg



# Set page configuration
st.set_page_config(page_title="Full Time App", page_icon="🌍", layout="centered")

with st.container(border=True):  
# Header and section selector
    st.image('./media/Full-Time Workers.jpg')

with st.container(border=True):     
    reg()
  
       

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}  /* Hide the hamburger menu */
    footer {visibility: hidden;}  /* Hide the default footer */
    header {visibility: hidden;}  /* Hide the header */
    
    /* Custom footer styling - LEFT ALIGNED */
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: white;
        text-align: left;
        padding: 15px 20px;
        font-family: Arial, sans-serif;
        font-size: 14px;
        border-top: 1px solid #444;
        z-index: 999;
    }
    
    /* Ensure content doesn't hide behind fixed footer */
    .main .block-container {
        padding-bottom: 70px;
    }
    </style>
    
    <!-- Custom Footer -->
    <div class="custom-footer">
        DCLM Full-Time Workers New Year Evaluation Meeting
    </div>
    """,
    unsafe_allow_html=True
)