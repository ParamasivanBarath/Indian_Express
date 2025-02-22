import streamlit as st
from database_operations import DatabaseOperations
from .blog_convertor import show_blog_conversion

def show_social_media(assistant):
    st.header("📱 Social Media Content Generator")
    db_ops = DatabaseOperations()
    
    article = st.text_area("Article Content", height=200)
    platforms = st.multiselect("Select Platforms", 
                             ["Twitter", "LinkedIn", "Facebook", "Instagram"], 
                             key="platforms")
    
    if st.button("Generate Social Posts", key="gen_social") and platforms:
        with st.spinner("Creating social media content..."):
            posts = assistant.generate_social_posts(article, platforms)
            article_id = db_ops.save_article("Social", "Posts", article, len(article.split()))
            post_id = db_ops.save_social_post(article_id, ",".join(platforms), posts, "")
            st.markdown(posts)
            st.download_button("Download Social Posts", posts, "social_posts.txt", 
                             key="download_social")
            show_blog_conversion(assistant, posts, post_id, "social")
