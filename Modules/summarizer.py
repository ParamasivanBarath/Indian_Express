import streamlit as st
from database_operations import DatabaseOperations
from .blog_convertor import show_blog_conversion

def show_summarizer(assistant):
    st.header("📊 Enhanced Summarizer")
    db_ops = DatabaseOperations()
    
    article = st.text_area("Article Content", height=300)
    col1, col2 = st.columns(2)
    with col1:
        summary_style = st.selectbox("Summary Style", 
                                   ["Bullet Points", "Executive Summary", 
                                    "Key Takeaways", "Abstract"], 
                                   key="summary_style")
    with col2:
        summary_length = st.select_slider("Summary Length", 
                                        options=["short", "medium", "long"], 
                                        key="summary_length")
    
    if st.button("Generate Summary", key="gen_summary"):
        with st.spinner("Creating summary..."):
            summary = assistant.create_summary(article, summary_style, summary_length)
            article_id = db_ops.save_article("Summary", "Summary", article, 
                                           len(article.split()))
            summary_id = db_ops.save_summary(article_id, summary_style, summary, 
                                           summary_length)
            st.markdown(summary)
            st.download_button("Download Summary", summary, "summary.txt", 
                             key="download_summary")
            
            show_blog_conversion(assistant, summary, summary_id, "summary")
