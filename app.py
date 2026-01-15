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
    #MainMenu {visibility: hidden;}  # Hide the hamburger menu
    footer {visibility: hidden;}  # Hide the footer
    header {visibility: hidden;}  # Hide the header
    </style>
    """,
    unsafe_allow_html=True
)


