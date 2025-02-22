import streamlit as st
from database_operations import DatabaseOperations
from .blog_convertor import show_blog_conversion

def show_content_verification(assistant):
    st.header("✅ Advanced Content Verification")
    db_ops = DatabaseOperations()
    
    text = st.text_area("Content to Verify", height=300)
    
    if st.button("Verify Content", key="verify_content"):
        with st.spinner("Performing comprehensive analysis..."):
            analysis = assistant.verify_content(text)
            verification_id = db_ops.save_verification(text, analysis)
            st.markdown(analysis)
            st.download_button("Download Analysis", analysis, "analysis.txt", 
                             key="download_analysis")
            show_blog_conversion(assistant, analysis, verification_id, "verification")
