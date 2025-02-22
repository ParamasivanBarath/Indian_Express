import streamlit as st
from database_operations import DatabaseOperations
from .blog_convertor import show_blog_conversion

def show_headlines_seo(assistant):
    st.header("🎯 Headlines & SEO Generator")
    db_ops = DatabaseOperations()
    
    article = st.text_area("Article Content", height=200)
    target_platform = st.selectbox("Target Platform", 
                                 ["General", "News Website", "Social Media", 
                                  "Search Engines", "Mobile Apps"])
    
    if st.button("Generate Headlines", key="gen_headlines"):
        with st.spinner("Generating optimized headlines..."):
            headlines = assistant.generate_headlines(article, target_platform)
            article_id = db_ops.save_article("Headlines", "SEO", article, len(article.split()))
            headline_id = db_ops.save_headline(article_id, target_platform, headlines, "")
            st.markdown(headlines)
            st.download_button("Download Headlines", headlines, "headlines.txt", 
                             key="download_headlines")
            show_blog_conversion(assistant, headlines, headline_id, "headlines")
