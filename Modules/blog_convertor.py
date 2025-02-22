import streamlit as st
from database_operations import DatabaseOperations
from utils import show_blog_content
from datetime import datetime

def show_blog_conversion(assistant, content, source_id, source_type):
    db_ops = DatabaseOperations()
    
    st.markdown("### Convert to Blog Format")
    
    # Blog Form Container
    with st.form(key=f"blog_form_{source_type}"):
        # Title Input
        blog_title = st.text_input(
            "Blog Title", 
            value=f"{source_type.title()} Blog", 
            key=f"blog_title_{source_type}"
        )
        
        # Subtitle Input
        blog_subtitle = st.text_input(
            "Blog Subtitle", 
            value="Indian Express", 
            key=f"blog_subtitle_{source_type}"
        )
        
        # Content Preview
        st.text_area(
            "Content Preview", 
            value=content,
            height=200,
            disabled=True
        )
        
        # Status Selection
        status = st.selectbox(
            "Publication Status",
            options=["draft", "published", "archived"],
            index=1  # Default to "published"
        )
        
        # Submit Button - Must be the last element inside the form
        submitted = st.form_submit_button("Convert to Blog")
        
    # Form submission handling - Must be outside the form
    if submitted:
        try:
            with st.spinner("Converting to blog format..."):
                # Convert content to blog format
                blog_post = assistant.convert_to_blog(content, blog_title, blog_subtitle)
                
                # Prepare blog data
                blog_data = {
                    'title': blog_title,
                    'subtitle': blog_subtitle,
                    'content': blog_post,
                    'source_type': source_type,
                    'source_id': source_id,
                    'status': status
                }
                
                # Save blog entry
                blog_id = db_ops.save_blog(**blog_data)
                
                current_time = datetime.now()
                
                # Update session state
                st.session_state.update({
                    "blog_title": blog_title,
                    "blog_subtitle": blog_subtitle,
                    "blog_post": blog_post,
                    "blog_id": blog_id,
                    "source_type": source_type,
                    "source_id": source_id,
                    "created_at": current_time,
                    "status": status
                })
                
                st.success(f"""Blog post created successfully!
                          Title: {blog_title}
                          Status: {status}
                          Created on: {current_time.strftime('%B %d, %Y %I:%M %p')}""")
                
                # Get all blogs for today
                today_blogs = db_ops.get_blogs_by_date(current_time.date())
                if today_blogs:
                    st.info(f"Total blogs created today: {len(today_blogs)}")
                
                show_blog_content()
                
        except Exception as e:
            st.error(f"Error converting to blog: {str(e)}")
            st.error(f"Details: Source Type - {source_type}, Source ID - {source_id}")
