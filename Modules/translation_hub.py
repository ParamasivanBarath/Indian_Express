import streamlit as st
from database_operations import DatabaseOperations
from .blog_convertor import show_blog_conversion


def show_translation_hub(assistant):
    st.header("🌍 Translation Hub")
    db_ops = DatabaseOperations()
    
    text = st.text_area("Content to translate", height=200)
    target_language = st.selectbox("Target Language", 
                                 ["Spanish", "French", "German", "Italian", 
                                  "Chinese", "Japanese", "Hindi", "Tamil"], 
                                 key="target_language")
    preserve_format = st.checkbox("Preserve Formatting", value=True, 
                                key="preserve_format")
    
    if st.button("Translate", key="translate"):
        with st.spinner("Translating content..."):
            translation = assistant.translate_content(text, target_language, preserve_format)
            translation_id = db_ops.save_translation(text, translation, target_language)
            st.markdown(translation)
            st.download_button("Download Translation", translation, "translation.txt", 
                             key="download_translation")
            show_blog_conversion(assistant, translation, translation_id, "translation")
