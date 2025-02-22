import streamlit as st

def local_css():
    css = """
    <style>
    body {
        font-family: 'Georgia', serif;
        background-color: #f7f7f7;
        color: #333;
    }
    .header {
        background-color: #b30000;
        padding: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .blog-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 1rem 0 0.2rem 0;
    }
    .blog-subtitle {
        font-size: 1.5rem;
        color: #555;
        margin-bottom: 1rem;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
