import streamlit as st

def show_blog_content():
    if not hasattr(st.session_state, 'show_blog'):
        st.session_state.show_blog = False
    st.session_state.show_blog = True
    st.experimental_rerun()

def clear_blog_state():
    keys_to_clear = ["blog_title", "blog_subtitle", "blog_post", "show_blog"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
